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
2. Search current job sources. Use employer careers pages and direct links to employer-controlled or authorized ATS postings (for example Workday, Greenhouse, Lever, SmartRecruiters) as primary verification sources. Search engines, aggregators and social platforms may provide leads but are not sufficient proof that a job remains open.
3. For every candidate, open the actual employer/authorized listing where accessible. Check the position title, employer, location, remote policy, advertised seniority, required skills, application link, requisition ID if available, and whether the vacancy is currently available. Record the date/time of verification. If the source cannot be accessed or the opening cannot be verified, put it in a separate **unverified leads** section rather than the verified shortlist.
   Keep the search bounded: a few sources and at most about ten candidates. When a source returns 403/429 or needs sign-in, do not retry it; after two blocked sources or no verifiable listing, stop searching and report what you have.
4. Deduplicate syndicated postings and reposts by employer, requisition ID and canonical URL. Exclude obviously closed, expired or inconsistent postings. Never infer a salary, visa policy or fully remote status from silence.
5. Assess each job against demonstrated skills, desired professional direction, hard constraints, and explicit stretch areas. Explain positives, gaps and risk of mismatch. Do not equate keyword similarity with fit or recommend people-management roles by default.
6. Return a ranked shortlist with direct application URLs, evidence and relevant dates. Surface uncertainty, and optionally suggest a tailored resume using `build-resume` when installed. Do not auto-apply, upload private documents or contact employers without express permission.

## Output: Verified Job Shortlist

For each verified listing: title; employer; location and working arrangement (as published); canonical employer/ATS URL; requisition ID when available; verified-at timestamp; relevant requirements; strong matches; meaningful gaps; any known hard-constraint conflicts; concise fit rationale.

Add a clearly separated section of unverified leads only if useful. If no postings can be verified, report that result and the scope/time of the search—do not fabricate openings.

When the workspace has a root `README.md` index, add a link to each new record under `Records`.

## Done when

- Each **verified** job has a current first-party employer or authorized ATS listing and a direct application path.
- User constraints are respected, and unknown conditions stay unknown.
- Duplicate and expired listings do not pollute the verified shortlist.
- Fit assessments distinguish observed experience, transferable skills and stretch gaps.
- The result includes verification timestamps and direct source links.
- No job application, message or external mutation occurs without authorization.

