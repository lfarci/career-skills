# Job sources

Tested from a Linux box with a plain HTTP client on 2026-10-29. Re-check when a source fails; sites change.

## Fallback order

1. **Host job tools**: a job-search connector/MCP the host already has (e.g. Indeed's official MCP, a LinkedIn MCP driving the user's own session, Adzuna MCP, Himalayas MCP). Use its search, then verify on the employer's page.
2. **Host web search and page fetch / signed-in browser**: search `"<role>" <city> site:<board>` and open results one at a time. Use the user's own browser session for sign-in sites only when the host provides one and the user agrees.
3. **`scripts/search_jobs.py`**: public ATS board APIs for saved companies, Remotive/Arbeitnow feeds, Adzuna when keyed, JSON-LD from a job URL.
4. **User paste/export**: ask the user to paste a listing or saved-search alert email from a site that blocks you (LinkedIn, Indeed, StepStone, Jobat).
5. **Stop**: after two blocked sources or no verifiable listing, report what you have.

## Tier 1: employer-controlled, machine-readable (counts as verified)

| Source | Access | Key | Tested |
|---|---|---|---|
| Greenhouse | `boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true` | no | 200 JSON (showpad, collibra, datadog, doctolib) |
| Lever | `api.lever.co/v0/postings/<slug>?mode=json` (EU: `api.eu.lever.co`) | no | 200 JSON (spotify) |
| Ashby | `api.ashbyhq.com/posting-api/job-board/<slug>` | no | 200 JSON (ramp, alan) |
| Recruitee | `<slug>.recruitee.com/api/offers/` | no | 200 JSON (dataroots, intigriti) |
| SmartRecruiters | `api.smartrecruiters.com/v1/companies/<slug>/postings` | no | 200 JSON (BoschGroup, Ubisoft2) |
| Personio | `<slug>.jobs.personio.de/xml` | no | 200 XML (empty for test slugs) |
| Workable | `apply.workable.com/api/v1/widget/accounts/<slug>` | no | 404 for guessed slugs; works only with the exact account slug |
| schema.org `JobPosting` JSON-LD | in the HTML of many employer/ATS job pages (Lever job pages have it) | no | `--url`; skips postings past `validThrough` |

Find a slug from the careers page's "Apply" links (`boards.greenhouse.io/<slug>`, `jobs.lever.co/<slug>`, `jobs.ashbyhq.com/<slug>`, `<slug>.recruitee.com`, `jobs.smartrecruiters.com/<slug>`, `<slug>.jobs.personio.de`, `apply.workable.com/<slug>`), with `--detect <careers URL>` (only when links are in the HTML), or `--probe "<Company>"` (7 requests; confirm the board belongs to that company).

## Tier 2: aggregator feeds (leads; verify on the employer page)

| Source | Access | Key | Region | Tested |
|---|---|---|---|---|
| Remotive | `remotive.com/api/remote-jobs?search=` | no; link back, low volume | remote, global | 200 JSON |
| Arbeitnow | `arbeitnow.com/api/job-board-api` | no | EU (DE-heavy), remote | 200 JSON |
| Adzuna | `api.adzuna.com/v1/api/jobs/be/search/1` (also fr, nl, de…) | **free** app id/key at developer.adzuna.com: set `ADZUNA_APP_ID`, `ADZUNA_APP_KEY` | BE, FR, NL… | 400 without key |
| Himalayas, Jobicy, RemoteOK, We Work Remotely RSS | JSON / RSS | no | remote | 200 (not in script; use via host fetch) |
| France Travail "Offres d'emploi" API | OAuth client credentials | free account at francetravail.io | FR | 401 without key |
| EURES, VDAB, Le Forem | web portals; VDAB/Forem open-data APIs need partner registration | partner | BE, EU | pages 200 (JS-rendered) |
| Free-Work | listing pages `free-work.com/fr/tech-it/jobs?query=` (freelance + CDI, FR/BE) | no | FR, BE | 200 HTML; use host fetch |
| ICTJob.be | `ictjob.be/fr/chercher-emplois-it?keywords=` | no | BE IT | 200 HTML; use host fetch |
| Welcome to the Jungle | `welcometothejungle.com/fr/jobs?query=` | no | FR, BE | 200 HTML, JS-rendered |

## Tier 3: blocked or sign-in (leads only, never scripted)

| Source | Tested | How to use |
|---|---|---|
| LinkedIn | public guest pages 200, but robots.txt disallows `/jobs-guest/` and the ToS forbid scraping | host web search results, the user's own signed-in browser, a LinkedIn MCP in the user's session, or the user's job-alert emails/pastes; open the employer's page to verify |
| Indeed | 403 | official Indeed MCP (Claude connector, Indeed account) or user paste |
| StepStone.be, Jobat.be, Glassdoor | 403 | host search snippets, user paste or alert emails |
| Employer sites behind bot protection (e.g. Devoteam 403, Easi 429) | blocked | look for their ATS board instead; do not retry |

## Belgium / France tech starting set

LinkedIn, Indeed, StepStone, Jobat, ICTJob.be, VDAB (NL), Le Forem (FR), Actiris (Brussels), Free-Work, Welcome to the Jungle, EURES, plus ATS boards of saved companies. Language filtering: pass `--exclude Dutch,Nederlands,néerlandais` only when the user cannot work in Dutch.
