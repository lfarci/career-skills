---
name: find-jobs
description: Find current job vacancies suited to a person's professional profile, skills, goals and constraints, verify each opening from an employer or authorized recruiting source, and rank opportunities transparently. Use when the person asks for matching jobs, vacancies, roles to apply for, or an employer-specific opening search.
---

# Find Matching Jobs

Find *live, verifiable* openings—not just roles that sound suitable. Search broadly, verify narrowly, and explain match quality without overstating certainty.

## Workspace
Read the chosen career workspace index and relevant canonical records when available. Follow its source map and privacy/write boundaries; link evidence and outputs instead of duplicating them. Without an index, use supplied inputs and ask only task-relevant gaps. Work with Markdown wherever stored; do not require setup, a provider or folder migration.

## Steps

1. Read the user's career record or supplied resume, confirmed preferences and constraints. Capture target functions, seniority, locations/time zones, remote/hybrid preferences, languages, employment eligibility, compensation expectations and exclusions **only when known**. Ask one targeted question if a missing hard constraint prevents useful searching; otherwise use declared assumptions.
2. Search current job sources. Use employer careers pages and direct links to employer-controlled or authorized ATS postings (for example Workday, Greenhouse, Lever, SmartRecruiters) as primary verification sources. Search engines, aggregators and social platforms may provide leads but are not sufficient proof that a job remains open.
3. For every candidate, open the actual employer/authorized listing where accessible. Check the position title, employer, location, remote policy, advertised seniority, required skills, application link, requisition ID if available, and whether the vacancy is currently available. Record the date/time of verification. If the source cannot be accessed or the opening cannot be verified, put it in a separate **unverified leads** section rather than the verified shortlist.
4. Deduplicate syndicated postings and reposts by employer, requisition ID and canonical URL. Exclude obviously closed, expired or inconsistent postings. Never infer a salary, visa policy or fully remote status from silence.
5. Assess each job against demonstrated skills, desired professional direction, hard constraints, and explicit stretch areas. Explain positives, gaps and risk of mismatch. Do not equate keyword similarity with fit or recommend people-management roles by default.
6. Return a ranked shortlist with direct application URLs, evidence and relevant dates. Surface uncertainty, and optionally suggest a tailored resume using `build-resume` when installed. Do not auto-apply, upload private documents or contact employers without express permission.

## Output: Verified Job Shortlist

For each verified listing: title; employer; location and working arrangement (as published); canonical employer/ATS URL; requisition ID when available; verified-at timestamp; relevant requirements; strong matches; meaningful gaps; any known hard-constraint conflicts; concise fit rationale.

Add a clearly separated section of unverified leads only if useful. If no postings can be verified, report that result and the scope/time of the search—do not fabricate openings.

## Done when

- Each **verified** job has a current first-party employer or authorized ATS listing and a direct application path.
- User constraints are respected, and unknown conditions stay unknown.
- Duplicate and expired listings do not pollute the verified shortlist.
- Fit assessments distinguish observed experience, transferable skills and stretch gaps.
- The result includes verification timestamps and direct source links.
- No job application, message or external mutation occurs without authorization.

