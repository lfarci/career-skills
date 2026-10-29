#!/usr/bin/env python3
"""Search keyless job sources and print normalized, filtered openings.

Sources: public ATS job-board APIs (Greenhouse, Lever, Ashby, Workable,
Recruitee, SmartRecruiters, Personio), Remotive and Arbeitnow feeds, Adzuna
when ADZUNA_APP_ID/ADZUNA_APP_KEY are set, and schema.org JobPosting JSON-LD
on a given page. ATS and JSON-LD results come from the employer's own board
(Status: open); aggregator results are leads (Status: unverified).

Exit codes: 0 openings found, 1 no openings, 2 unusable input.
Python 3 standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Callable

USER_AGENT = "career-skills-find-jobs/1.0 (personal job search; +https://github.com/lfarci/career-skills)"
TIMEOUT = 20
DELAY = 1.0
REMOTE_REGIONS = ("worldwide", "anywhere", "europe", "emea", "eu", "belgium", "cet")
ATS = ("greenhouse", "lever", "ashby", "workable", "recruitee", "smartrecruiters", "personio")
BOARD_LINE = re.compile(r"^Jobs board:\s*([a-z]+):([\w.-]+)", re.IGNORECASE | re.MULTILINE)


class FetchError(Exception):
    """A source could not be fetched; the message says why (e.g. HTTP 403)."""


def now_iso() -> str:
    """Return the current UTC time as YYYY-MM-DDTHH:MMZ."""
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def strip_html(text: str | None, limit: int = 600) -> str:
    """Return plain text from an HTML fragment, truncated to limit chars."""
    plain = re.sub(r"<[^>]+>", " ", html.unescape(text or ""))
    return re.sub(r"\s+", " ", plain).strip()[:limit]


_last_request = [0.0]


def fetch(url: str, accept: str = "application/json") -> str:
    """GET url politely (one request per DELAY seconds) and return the body."""
    wait = DELAY - (time.monotonic() - _last_request[0])
    if wait > 0:
        time.sleep(wait)
    _last_request[0] = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        raise FetchError(f"HTTP {exc.code}") from None
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise FetchError(f"network error: {getattr(exc, 'reason', exc)}") from None


def job(source: str, company: str, title: str, url: str, location: str = "",
        remote: bool | None = None, apply: str = "", posted: str = "",
        description: str = "", status: str = "open", tags: list[str] | None = None) -> dict[str, Any]:
    """Build one normalized job dict."""
    return {"title": (title or "").strip(), "company": (company or "").strip(),
            "location": (location or "").strip(), "remote": remote, "url": url,
            "apply": apply or url, "posted": posted or "", "source": source,
            "status": status, "tags": tags or [], "description": strip_html(description)}


def _remote_from(text: str) -> bool | None:
    return True if re.search(r"\bremote\b|télétravail|full[- ]?remote", text or "", re.I) else None


# --- ATS parsers: payload -> jobs -------------------------------------------

def parse_greenhouse(data: dict, company: str) -> list[dict]:
    """Parse boards-api.greenhouse.io /jobs?content=true."""
    return [job("greenhouse", company, j.get("title", ""), j.get("absolute_url", ""),
                (j.get("location") or {}).get("name", ""), _remote_from((j.get("location") or {}).get("name", "")),
                posted=(j.get("updated_at") or "")[:10], description=j.get("content", ""))
            for j in data.get("jobs", [])]


def parse_lever(data: list, company: str) -> list[dict]:
    """Parse api.lever.co/v0/postings/<slug>?mode=json."""
    out = []
    for j in data:
        cat = j.get("categories") or {}
        loc = cat.get("location") or ", ".join(cat.get("allLocations") or [])
        wt = (j.get("workplaceType") or "").lower()
        remote = True if wt == "remote" else (False if wt == "onsite" else _remote_from(loc))
        posted = dt.datetime.fromtimestamp(j["createdAt"] / 1000, dt.timezone.utc).strftime("%Y-%m-%d") if j.get("createdAt") else ""
        out.append(job("lever", company, j.get("text", ""), j.get("hostedUrl", ""), loc, remote,
                       j.get("applyUrl", ""), posted, j.get("descriptionPlain", ""), tags=[cat.get("team", "")]))
    return out


def parse_ashby(data: dict, company: str) -> list[dict]:
    """Parse api.ashbyhq.com/posting-api/job-board/<slug>."""
    return [job("ashby", company, j.get("title", ""), j.get("jobUrl", ""), j.get("location", ""),
                j.get("isRemote"), j.get("applyUrl", ""), (j.get("publishedAt") or "")[:10],
                j.get("descriptionPlain", ""), tags=[j.get("department", "")])
            for j in data.get("jobs", []) if j.get("isListed", True)]


def parse_workable(data: dict, company: str) -> list[dict]:
    """Parse apply.workable.com/api/v1/widget/accounts/<slug>."""
    name = data.get("name") or company
    out = []
    for j in data.get("jobs", []):
        loc = ", ".join(x for x in (j.get("city"), j.get("country")) if x)
        out.append(job("workable", name, j.get("title", ""), j.get("url") or j.get("shortlink", ""), loc,
                       j.get("telecommuting"), j.get("application_url", ""), j.get("published_on", ""),
                       tags=[j.get("department", "")]))
    return out


def parse_recruitee(data: dict, company: str) -> list[dict]:
    """Parse <slug>.recruitee.com/api/offers/."""
    return [job("recruitee", j.get("company_name") or company, j.get("title", ""), j.get("careers_url", ""),
                j.get("location", ""), j.get("remote"), j.get("careers_apply_url", ""),
                (j.get("published_at") or "")[:10], j.get("description", ""), tags=[j.get("department") or ""])
            for j in data.get("offers", []) if j.get("status", "published") == "published"]


def parse_smartrecruiters(data: dict, company: str) -> list[dict]:
    """Parse api.smartrecruiters.com/v1/companies/<slug>/postings."""
    out = []
    for j in data.get("content", []):
        loc = j.get("location") or {}
        where = ", ".join(x for x in (loc.get("city"), loc.get("country", "").upper()) if x)
        slug = (j.get("company") or {}).get("identifier", company)
        url = f"https://jobs.smartrecruiters.com/{slug}/{j.get('id', '')}"
        out.append(job("smartrecruiters", (j.get("company") or {}).get("name") or company, j.get("name", ""), url,
                       where, loc.get("remote"), posted=(j.get("releasedDate") or "")[:10]))
    return out


def parse_personio(text: str, company: str, slug: str) -> list[dict]:
    """Parse <slug>.jobs.personio.de/xml."""
    out = []
    for pos in ET.fromstring(text).iter("position"):
        get = lambda tag: (pos.findtext(tag) or "").strip()  # noqa: E731
        url = f"https://{slug}.jobs.personio.de/job/{get('id')}"
        out.append(job("personio", get("subcompany") or company, get("name"), url, get("office"),
                       _remote_from(get("office")), posted=get("createdAt")[:10], tags=[get("department")]))
    return out


def board_url(ats: str, slug: str) -> str:
    """Return the public API URL for an ATS board."""
    q = urllib.parse.quote(slug)
    return {
        "greenhouse": f"https://boards-api.greenhouse.io/v1/boards/{q}/jobs?content=true",
        "lever": f"https://api.lever.co/v0/postings/{q}?mode=json",
        "ashby": f"https://api.ashbyhq.com/posting-api/job-board/{q}",
        "workable": f"https://apply.workable.com/api/v1/widget/accounts/{q}",
        "recruitee": f"https://{q}.recruitee.com/api/offers/",
        "smartrecruiters": f"https://api.smartrecruiters.com/v1/companies/{q}/postings?limit=100",
        "personio": f"https://{q}.jobs.personio.de/xml",
    }[ats]


def search_board(ats: str, slug: str, company: str, get: Callable[..., str] = fetch) -> list[dict]:
    """Fetch and parse one ATS board."""
    url = board_url(ats, slug)
    if ats == "personio":
        return parse_personio(get(url, "application/xml"), company, slug)
    data = json.loads(get(url))
    return globals()[f"parse_{ats}"](data, company)


BOARD_PATTERNS = (
    ("greenhouse", r"(?:boards|job-boards)(?:\.eu)?\.greenhouse\.io/(?:embed/job_board\?for=)?([\w-]+)"),
    ("lever", r"jobs\.(?:eu\.)?lever\.co/([\w.-]+)"),
    ("ashby", r"jobs\.ashbyhq\.com/([\w.-]+)"),
    ("workable", r"apply\.workable\.com/([\w-]+)"),
    ("recruitee", r"([\w-]+)\.recruitee\.com"),
    ("smartrecruiters", r"(?:jobs|careers)\.smartrecruiters\.com/([\w-]+)"),
    ("personio", r"([\w-]+)\.jobs\.personio\.(?:de|com)"),
)
IGNORED_SLUGS = {"embed", "api", "www", "v1", "jobs", "careers", "static"}


def detect_boards(page: str) -> list[str]:
    """Return ats:slug specs for ATS board links found in a careers page."""
    found: list[str] = []
    for ats, pattern in BOARD_PATTERNS:
        for slug in re.findall(pattern, page, re.I):
            spec = f"{ats}:{slug}"
            if slug.lower() not in IGNORED_SLUGS and spec not in found:
                found.append(spec)
    return found


def probe_boards(name: str, get: Callable[..., str] = fetch) -> list[str]:
    """Try each ATS API with a slug guessed from a company name; return boards with openings."""
    slug = re.sub(r"[^a-z0-9-]", "", name.lower().replace(" ", ""))
    found = []
    for ats in ATS:
        try:
            if search_board(ats, slug, name, get):
                found.append(f"{ats}:{slug}")
        except (FetchError, ValueError, ET.ParseError, KeyError, TypeError):
            continue
    return found


# --- Aggregators (leads) ------------------------------------------------------

def parse_remotive(data: dict) -> list[dict]:
    """Parse remotive.com/api/remote-jobs (leads; link back to Remotive)."""
    return [job("remotive", j.get("company_name", ""), j.get("title", ""), j.get("url", ""),
                j.get("candidate_required_location", ""), True, posted=(j.get("publication_date") or "")[:10],
                description=j.get("description", ""), status="unverified", tags=j.get("tags") or [])
            for j in data.get("jobs", [])]


def parse_arbeitnow(data: dict) -> list[dict]:
    """Parse arbeitnow.com/api/job-board-api (leads)."""
    out = []
    for j in data.get("data", []):
        posted = dt.datetime.fromtimestamp(j["created_at"], dt.timezone.utc).strftime("%Y-%m-%d") if j.get("created_at") else ""
        out.append(job("arbeitnow", j.get("company_name", ""), j.get("title", ""), j.get("url", ""),
                       j.get("location", ""), j.get("remote"), posted=posted,
                       description=j.get("description", ""), status="unverified", tags=j.get("tags") or []))
    return out


def parse_adzuna(data: dict) -> list[dict]:
    """Parse api.adzuna.com/v1/api/jobs/<country>/search (leads)."""
    return [job("adzuna", (j.get("company") or {}).get("display_name", ""), j.get("title", ""),
                j.get("redirect_url", ""), (j.get("location") or {}).get("display_name", ""),
                _remote_from(j.get("title", "") + " " + j.get("description", "")),
                posted=(j.get("created") or "")[:10], description=j.get("description", ""), status="unverified")
            for j in data.get("results", [])]


def search_feeds(keywords: list[str], locations: list[str], country: str,
                 get: Callable[..., str] = fetch) -> tuple[list[dict], list[str]]:
    """Query the aggregator feeds; return (jobs, errors)."""
    jobs: list[dict] = []
    errors: list[str] = []
    term = " ".join(keywords[:1]) if keywords else ""
    calls = [("remotive", "https://remotive.com/api/remote-jobs?" + urllib.parse.urlencode({"search": term} if term else {}), parse_remotive),
             ("arbeitnow", "https://www.arbeitnow.com/api/job-board-api", parse_arbeitnow)]
    app_id, app_key = os.environ.get("ADZUNA_APP_ID"), os.environ.get("ADZUNA_APP_KEY")
    if app_id and app_key:
        params = {"app_id": app_id, "app_key": app_key, "results_per_page": 50, "what_or": " ".join(keywords)}
        if locations:
            params["where"] = locations[0]
        calls.append(("adzuna", f"https://api.adzuna.com/v1/api/jobs/{country}/search/1?" + urllib.parse.urlencode(params), parse_adzuna))
    for name, url, parser in calls:
        try:
            jobs += parser(json.loads(get(url)))
        except (FetchError, ValueError) as exc:
            errors.append(f"{name}: {exc}")
    return jobs, errors


# --- JSON-LD ------------------------------------------------------------------

def _postings(node: Any) -> list[dict]:
    if isinstance(node, list):
        return [p for item in node for p in _postings(item)]
    if not isinstance(node, dict):
        return []
    kind = node.get("@type")
    if kind == "JobPosting" or (isinstance(kind, list) and "JobPosting" in kind):
        return [node]
    return _postings(node.get("@graph", []))


def parse_jsonld(page: str, url: str, today: dt.date | None = None) -> list[dict]:
    """Extract schema.org JobPosting objects from an HTML page."""
    today = today or dt.date.today()
    out = []
    for block in re.findall(r"<script[^>]+application/ld\+json[^>]*>(.*?)</script>", page, re.S | re.I):
        try:
            data = json.loads(html.unescape(block.strip()))
        except ValueError:
            continue
        for p in _postings(data):
            org = p.get("hiringOrganization") or {}
            locs = p.get("jobLocation") or []
            locs = locs if isinstance(locs, list) else [locs]
            where = ", ".join(x for loc in locs for x in [
                ((loc.get("address") or {}) if isinstance(loc, dict) else {}).get("addressLocality", "")] if x)
            remote = True if p.get("jobLocationType") == "TELECOMMUTE" else None
            status = "open"
            valid = (p.get("validThrough") or "")[:10]
            if valid:
                try:
                    status = "closed" if dt.date.fromisoformat(valid) < today else "open"
                except ValueError:
                    pass
            out.append(job("jsonld", org.get("name", "") if isinstance(org, dict) else str(org), p.get("title", ""),
                           p.get("url") or url, where, remote, posted=(p.get("datePosted") or "")[:10],
                           description=p.get("description", ""), status=status))
    return out


# --- Criteria, dedupe, seen ---------------------------------------------------

def read_boards(career: Path) -> list[tuple[str, str, str]]:
    """Return (ats, slug, company) from research/companies/*.md 'Jobs board:' lines."""
    boards = []
    for record in sorted((career / "research" / "companies").glob("*.md")):
        text = record.read_text(encoding="utf-8")
        title = re.search(r"^#\s+(.+)$", text, re.M)
        for ats, slug in BOARD_LINE.findall(text):
            boards.append((ats.lower(), slug, title.group(1).strip() if title else slug))
    return boards


def _has(terms: list[str], text: str) -> bool:
    return any(re.search(r"(?<!\w)" + re.escape(t.lower()) + r"(?!\w)", text.lower()) for t in terms)


def matches(j: dict, keywords: list[str], locations: list[str], remote: bool, exclude: list[str]) -> bool:
    """Return True when a job fits keywords, location/remote and exclusions."""
    head = " ".join([j["title"]] + [t for t in j["tags"] if t])
    if keywords and not _has(keywords, head):
        return False
    if exclude and _has(exclude, j["title"] + " " + j["description"][:300]):
        return False
    if not locations:
        return True
    if _has(locations, j["location"]):
        return True
    return bool(remote and j["remote"] and (not j["location"] or _has(list(REMOTE_REGIONS), j["location"])))


def key(j: dict) -> str:
    """Return a dedupe key: canonical URL, else company+title+location."""
    url = j["url"].split("?")[0].rstrip("/").lower()
    return url or f"{j['company']}|{j['title']}|{j['location']}".lower()


def dedupe(jobs: list[dict]) -> list[dict]:
    """Drop duplicate URLs and same company+title+location reposts; prefer open over leads."""
    jobs = sorted(jobs, key=lambda j: j["status"] != "open")
    seen: set[str] = set()
    out = []
    for j in jobs:
        ids = {key(j), f"{j['company']}|{j['title']}|{j['location']}".lower()}
        if ids & seen:
            continue
        seen |= ids
        out.append(j)
    return out


def load_seen(path: Path | None) -> dict[str, str]:
    """Load the seen-file mapping key -> first-seen timestamp."""
    if not path or not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8")).get("seen", {})


def save_seen(path: Path, seen: dict[str, str]) -> None:
    """Write the seen-file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"seen": seen}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def to_markdown(jobs: list[dict], errors: list[str], checked: str) -> str:
    """Render jobs with the opportunity-record header fields."""
    lines = [f"# Job search ({checked})", ""]
    for j in jobs:
        flag = " (new)" if j.get("new") else ""
        lines += [f"## {j['title']}: {j['company']}{flag}", f"Status: {j['status']}", f"Checked: {checked}",
                  f"Source: {j['url']}", f"Apply: {j['apply']}",
                  f"Location: {j['location'] or 'unknown'}; remote: {'yes' if j['remote'] else 'unknown' if j['remote'] is None else 'no'}",
                  f"Found via: {j['source']}" + (f"; posted {j['posted']}" if j["posted"] else ""), ""]
    if not jobs:
        lines += ["No matching openings.", ""]
    if errors:
        lines += ["Source errors (not retried):"] + [f"- {e}" for e in errors]
    return "\n".join(lines).rstrip() + "\n"


def split(values: list[str] | None) -> list[str]:
    """Flatten repeated/comma-separated CLI values."""
    return [v.strip() for item in values or [] for v in item.split(",") if v.strip()]


def build_parser() -> argparse.ArgumentParser:
    """Return the CLI parser."""
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--career", type=Path, help="career/ root; reads 'Jobs board:' lines from research/companies/*.md")
    p.add_argument("--board", action="append", help="ATS board as ats:slug[:Company], e.g. greenhouse:datadog")
    p.add_argument("--url", action="append", help="job or careers page to read for JobPosting JSON-LD")
    p.add_argument("--detect", metavar="URL", help="print ats:slug boards linked from a careers page, then exit")
    p.add_argument("--probe", metavar="NAME", help="try every ATS API with a slug from NAME; print boards with openings")
    p.add_argument("--feeds", action="store_true", help="also query Remotive, Arbeitnow (and Adzuna when keyed)")
    p.add_argument("--keywords", action="append", help="title keywords, any match (comma-separated)")
    p.add_argument("--location", action="append", help="location terms, any match, e.g. Brussels,Bruxelles,Belgium")
    p.add_argument("--remote", action="store_true", help="also accept remote roles open to Europe/worldwide")
    p.add_argument("--exclude", action="append", help="drop titles/descriptions containing these terms")
    p.add_argument("--country", default="be", help="Adzuna country code (default be)")
    p.add_argument("--seen", type=Path, help="JSON seen-file; marks new results")
    p.add_argument("--only-new", action="store_true", help="print only results not in the seen-file")
    p.add_argument("--update-seen", action="store_true", help="add printed results to the seen-file")
    p.add_argument("--limit", type=int, default=30, help="max results (default 30)")
    p.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    return p


def main(argv: list[str] | None = None, get: Callable[..., str] = fetch) -> int:
    """Run the search; return the exit code."""
    args = build_parser().parse_args(argv)
    if args.detect:
        try:
            specs = detect_boards(get(args.detect, "text/html"))
        except FetchError as exc:
            print(f"error: {args.detect}: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(specs) if args.json else "\n".join(specs) or "No ATS board found.")
        return 0 if specs else 1
    if args.probe:
        specs = probe_boards(args.probe, get)
        print(json.dumps(specs) if args.json else "\n".join(specs) or "No ATS board found.")
        return 0 if specs else 1
    boards: list[tuple[str, str, str]] = []
    if args.career:
        if not (args.career / "research").is_dir():
            print(f"error: {args.career} has no research/ folder", file=sys.stderr)
            return 2
        boards += read_boards(args.career)
    for spec in args.board or []:
        parts = spec.split(":", 2)
        if len(parts) < 2 or parts[0].lower() not in ATS:
            print(f"error: bad --board {spec!r}; use ats:slug with ats in {', '.join(ATS)}", file=sys.stderr)
            return 2
        boards.append((parts[0].lower(), parts[1], parts[2] if len(parts) > 2 else parts[1]))
    if not (boards or args.url or args.feeds):
        print("error: give --career with Jobs board lines, --board, --url or --feeds", file=sys.stderr)
        return 2
    keywords, locations, exclude = split(args.keywords), split(args.location), split(args.exclude)
    jobs: list[dict] = []
    errors: list[str] = []
    for ats, slug, company in boards:
        try:
            jobs += search_board(ats, slug, company, get)
        except (FetchError, ValueError, ET.ParseError) as exc:
            errors.append(f"{ats}:{slug}: {exc}")
    for url in args.url or []:
        try:
            jobs += parse_jsonld(get(url, "text/html"), url)
        except FetchError as exc:
            errors.append(f"{url}: {exc}")
    if args.feeds:
        found, errs = search_feeds(keywords, locations, args.country, get)
        jobs += found
        errors += errs
    jobs = dedupe([j for j in jobs if j["status"] != "closed" and j["url"]
                   and matches(j, keywords, locations, args.remote, exclude)])[: args.limit]
    seen = load_seen(args.seen)
    checked = now_iso()
    for j in jobs:
        j["new"] = key(j) not in seen
    if args.only_new:
        jobs = [j for j in jobs if j["new"]]
    if args.seen and args.update_seen:
        for j in jobs:
            seen.setdefault(key(j), checked)
        save_seen(args.seen, seen)
    if args.json:
        print(json.dumps({"checked": checked, "jobs": jobs, "errors": errors}, indent=2, ensure_ascii=False))
    else:
        sys.stdout.write(to_markdown(jobs, errors, checked))
    return 0 if jobs else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
