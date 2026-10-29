---
name: find-jobs
description: Find and verify current job openings; rank roles against career evidence and working constraints.
---

# Find Matching Jobs

Find *live, verifiable* openings—not just roles that sound suitable. Search broadly, verify narrowly, and explain match quality without overstating certainty.

## Contract
- **Input:** profile/ capabilities, goals and constraints; selected company records and current employer/recruiter listings.
- **Scope:** Verify and compare specific vacancies; do not apply or generate unsolicited application materials.
- **Output:** Shortlist first; save selected roles to research/opportunities/<role>.md, linking company records and retaining requirements, sources, checked dates and fit.

## Steps

1. Read the user's career record or supplied resume, confirmed preferences and constraints. Capture target functions, seniority, locations/time zones, remote/hybrid preferences, languages, employment eligibility, compensation expectations and exclusions **only when known**. Ask one targeted question if a missing hard constraint prevents useful searching; otherwise use declared assumptions.
2. Search current job sources in the order of [sources](references/sources.md): the host's job-search connector or MCP when present, then the host's web search, page fetch or signed-in browser, then `scripts/search_jobs.py`, then asking the user to paste listings from sites that block you. Search engines, aggregators and social platforms (LinkedIn, Indeed) give leads; they are not proof that a job is open.
   Run the script (Python 3, no installs) with criteria from the profile, for example:
   `python3 scripts/search_jobs.py --career <career root> --keywords backend,cloud --location Brussels,Bruxelles,Belgium --remote --feeds`
   It reads `Jobs board: <ats>:<slug>` lines in research/companies/ records; add `--board greenhouse:<slug>`, `--url <job page>` (JSON-LD), `--json`. Exit 0 = results, 1 = none, 2 = bad input. Results with `Status: open` come from the employer's ATS; `unverified` ones are leads. Without Python, query the same URLs from the guide with the host's fetch tool.
3. For every candidate, open the actual employer/authorized listing where accessible (an ATS API result already is one). Check the position title, employer, location, remote policy, advertised seniority, required skills, application link, requisition ID if available, and whether the vacancy is currently available. Record the date/time of verification. If the source cannot be accessed or the opening cannot be verified, put it in a separate **unverified leads** section rather than the verified shortlist.
   Open pages one at a time with host tools; paging through a whole job board is out of scope. Keep the search bounded: a few sources and at most about ten candidates. When a source returns 403/429 or needs sign-in, do not retry it; after two blocked sources or no verifiable listing, stop searching and report what you have.
4. Deduplicate syndicated postings and reposts by employer, requisition ID and canonical URL. Exclude obviously closed, expired or inconsistent postings. Never infer a salary, visa policy or fully remote status from silence.
5. Assess each job against demonstrated skills, desired professional direction, hard constraints, and explicit stretch areas. Explain positives, gaps and risk of mismatch. Do not equate keyword similarity with fit or recommend people-management roles by default.
6. Return a ranked shortlist with direct application URLs, evidence and relevant dates. Surface uncertainty, and optionally suggest a tailored resume using `build-resume` when installed. Do not auto-apply, upload private documents or contact employers without express permission.

## Output: Verified Job Shortlist

Save each selected role with the [opportunity record](references/opportunity-record.md) header, linking its company record when one exists in research/companies/.


For each verified listing: title; employer; location and working arrangement (as published); canonical employer/ATS URL; requisition ID when available; verified-at timestamp; relevant requirements; strong matches; meaningful gaps; any known hard-constraint conflicts; concise fit rationale.

Add a clearly separated section of unverified leads only if useful. If no postings can be verified, report that result and the scope/time of the search—do not fabricate openings.

When the workspace has a root `README.md` index, add a link to each new record under `Records`.

## Recurring search

When the user asks for a scheduled search, use the host's scheduler or automation when it has one; otherwise suggest a system job the user installs themselves, running from the career root:

- cron (macOS/Linux): `0 8 * * 1-5 cd <career root> && python3 <skill dir>/scripts/search_jobs.py --career . --keywords backend --location Belgium --feeds --seen research/opportunities/.seen.json --only-new --update-seen >> research/opportunities/new-jobs.md`
- Windows Task Scheduler: `schtasks /Create /SC WEEKLY /D MON,WED,FRI /ST 08:00 /TN find-jobs /TR "cmd /c cd /d <career root> && python <skill dir>\scripts\search_jobs.py --career . --keywords backend --location Belgium --seen research\opportunities\.seen.json --only-new --update-seen >> research\opportunities\new-jobs.md"`

The seen-file keeps each run to new results only. A scheduled run only collects candidates; saving opportunity records still follows steps 3–6 in a session with the user.

## Done when

- Each **verified** job has a current first-party employer or authorized ATS listing and a direct application path.
- User constraints are respected, and unknown conditions stay unknown.
- Duplicate and expired listings do not pollute the verified shortlist.
- Fit assessments distinguish observed experience, transferable skills and stretch gaps.
- The result includes verification timestamps and direct source links.
- No job application, message or external mutation occurs without authorization.

