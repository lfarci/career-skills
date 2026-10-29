"""Tests for find-jobs/scripts/search_jobs.py (fixtures only, no network)."""
from __future__ import annotations

import contextlib
import datetime as dt
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "job-hunt" / "find-jobs" / "scripts" / "search_jobs.py"

GREENHOUSE = {"jobs": [
    {"title": "Senior Backend Engineer", "absolute_url": "https://boards.greenhouse.io/acme/jobs/1",
     "location": {"name": "Brussels, Belgium"}, "updated_at": "2026-10-01T10:00:00Z", "content": "&lt;p&gt;Python, AWS&lt;/p&gt;"},
    {"title": "Account Executive", "absolute_url": "https://boards.greenhouse.io/acme/jobs/2",
     "location": {"name": "Brussels, Belgium"}, "updated_at": "2026-10-01T10:00:00Z", "content": ""},
    {"title": "Backend Engineer", "absolute_url": "https://boards.greenhouse.io/acme/jobs/3",
     "location": {"name": "New York"}, "updated_at": "2026-10-01T10:00:00Z", "content": ""},
]}
LEVER = [{"text": "Cloud Engineer", "hostedUrl": "https://jobs.lever.co/acme/a", "applyUrl": "https://jobs.lever.co/acme/a/apply",
          "categories": {"location": "Remote - Europe", "team": "Platform"}, "workplaceType": "remote",
          "createdAt": 1790000000000, "descriptionPlain": "Kubernetes"}]
RECRUITEE = {"offers": [{"title": "Data Engineer", "careers_url": "https://acme.recruitee.com/o/data", "location": "Gent, Belgium",
                         "remote": False, "status": "published", "company_name": "Acme"}]}
REMOTIVE = {"jobs": [{"title": "Backend Developer", "company_name": "Far", "url": "https://remotive.com/x",
                      "candidate_required_location": "USA only", "publication_date": "2026-10-20"},
                     {"title": "Backend Developer", "company_name": "Near", "url": "https://remotive.com/y",
                      "candidate_required_location": "Europe", "publication_date": "2026-10-20"}]}
PERSONIO = """<?xml version="1.0"?><workzag-jobs><position><id>9</id><name>DevOps Engineer</name>
<office>Brussels</office><department>IT</department><createdAt>2026-10-02T00:00:00+00:00</createdAt></position></workzag-jobs>"""
JSONLD = """<html><script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"JobPosting",
"title":"Platform Engineer","hiringOrganization":{"name":"Acme"},"datePosted":"2026-10-10","validThrough":"2026-12-31",
"jobLocation":{"@type":"Place","address":{"addressLocality":"Brussels"}},"url":"https://acme.be/jobs/7"}]}</script>
<script type="application/ld+json">{"@type":"JobPosting","title":"Old role","validThrough":"2020-01-01","url":"https://acme.be/jobs/1"}</script></html>"""


def load():
    spec = importlib.util.spec_from_file_location("search_jobs", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SearchJobsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sj = load()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.calls: list[str] = []

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def fake_get(self, url: str, accept: str = "") -> str:
        self.calls.append(url)
        if "greenhouse" in url:
            return json.dumps(GREENHOUSE)
        if "lever.co" in url:
            return json.dumps(LEVER)
        if "recruitee" in url:
            return json.dumps(RECRUITEE)
        if "personio" in url:
            return PERSONIO
        if "remotive" in url:
            return json.dumps(REMOTIVE)
        if "acme.be" in url:
            return JSONLD
        raise self.sj.FetchError("HTTP 403")

    def run_main(self, *argv: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = self.sj.main(list(argv), get=self.fake_get)
        return code, out.getvalue()

    def test_parsers_normalize(self) -> None:
        gh = self.sj.parse_greenhouse(GREENHOUSE, "Acme")[0]
        self.assertEqual((gh["status"], gh["source"], gh["posted"]), ("open", "greenhouse", "2026-10-01"))
        self.assertEqual(gh["description"], "Python, AWS")
        lv = self.sj.parse_lever(LEVER, "Acme")[0]
        self.assertTrue(lv["remote"])
        self.assertEqual(lv["apply"], "https://jobs.lever.co/acme/a/apply")
        self.assertEqual(self.sj.parse_personio(PERSONIO, "Acme", "acme")[0]["url"], "https://acme.jobs.personio.de/job/9")
        self.assertEqual(self.sj.parse_remotive(REMOTIVE)[0]["status"], "unverified")

    def test_jsonld_graph_and_expired(self) -> None:
        jobs = self.sj.parse_jsonld(JSONLD, "https://acme.be/jobs", today=dt.date(2026, 10, 29))
        self.assertEqual([(j["title"], j["status"]) for j in jobs], [("Platform Engineer", "open"), ("Old role", "closed")])
        self.assertEqual(jobs[0]["location"], "Brussels")

    def test_filters_keywords_location_remote_exclude(self) -> None:
        code, out = self.run_main("--board", "greenhouse:acme:Acme", "--board", "lever:acme", "--feeds",
                                  "--keywords", "backend,cloud", "--location", "Brussels,Belgium", "--remote", "--json")
        self.assertEqual(code, 0)
        titles = {(j["title"], j["company"]) for j in json.loads(out)["jobs"]}
        self.assertEqual(titles, {("Senior Backend Engineer", "Acme"), ("Cloud Engineer", "acme"), ("Backend Developer", "Near")})
        code, out = self.run_main("--board", "greenhouse:acme", "--keywords", "backend", "--exclude", "senior",
                                  "--location", "Brussels", "--json")
        self.assertEqual(code, 1)

    def test_career_boards_and_errors(self) -> None:
        companies = self.root / "research" / "companies"
        companies.mkdir(parents=True)
        (companies / "acme.md").write_text("# Acme\n\nStatus: target\nJobs board: recruitee:acme\n", encoding="utf-8")
        (companies / "blocked.md").write_text("# Blocked\nJobs board: workable:blocked\n", encoding="utf-8")
        code, out = self.run_main("--career", str(self.root), "--location", "Belgium", "--json")
        data = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(data["jobs"][0]["company"], "Acme")
        self.assertEqual(data["errors"], ["workable:blocked: HTTP 403"])
        self.assertEqual(sum("blocked" in c for c in self.calls), 1, "blocked source must not be retried")

    def test_seen_file_marks_new(self) -> None:
        seen = self.root / "seen.json"
        args = ("--board", "recruitee:acme", "--seen", str(seen), "--only-new", "--update-seen", "--json")
        code, out = self.run_main(*args)
        self.assertEqual((code, len(json.loads(out)["jobs"])), (0, 1))
        code, out = self.run_main(*args)
        self.assertEqual((code, json.loads(out)["jobs"]), (1, []))

    def test_dedupe_prefers_employer_source(self) -> None:
        lead = self.sj.job("remotive", "Acme", "Dev", "https://acme.be/jobs/7?utm=x", status="unverified")
        open_ = self.sj.job("jsonld", "Acme", "Dev", "https://acme.be/jobs/7")
        self.assertEqual([j["source"] for j in self.sj.dedupe([lead, open_])], ["jsonld"])

    def test_detect_boards(self) -> None:
        page = '<a href="https://boards.greenhouse.io/acme/jobs/1">x</a> <a href="https://acme-be.recruitee.com/o/y">'
        self.assertEqual(self.sj.detect_boards(page), ["greenhouse:acme", "recruitee:acme-be"])

    def test_markdown_and_bad_input(self) -> None:
        code, out = self.run_main("--url", "https://acme.be/jobs")
        self.assertEqual(code, 0)
        self.assertIn("Status: open", out)
        self.assertNotIn("Old role", out)
        self.assertEqual(self.run_main("--board", "monster:acme")[0], 2)
        self.assertEqual(self.run_main()[0], 2)
        self.assertEqual(self.run_main("--career", str(self.root / "missing"))[0], 2)


if __name__ == "__main__":
    unittest.main()
