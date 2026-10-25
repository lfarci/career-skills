# Career workspace and skill lifecycle specification

Status: synthesized from the design conversation on 25 October 2026. Records agreed behavior and explicitly identifies deferred choices; it is not a claim that every behavior has been implemented or tested.

## Problem Statement

A professional needs a private, durable account of their career that agents can use to support reflection, growth, research and public presentation. Independent skills are less useful when they invent incompatible records, duplicate facts or confuse aspirations, approved wording and live published content.

The existing visual identity workflow also jumped too quickly into styles and logos, importing historical preferences before establishing the current request. Users had to reject unsuitable outputs instead of choosing meaningful concepts first.

The workspace must work with ordinary Markdown wherever the user stores it, respect an existing collection of notes, and make both reusable outputs and selected research easy to find. It must not turn into a mandatory database, platform integration or archive of every agent action.

## Solution

Use one entirely private career workspace with five clearly named homes:

| Home | Responsibility |
| --- | --- |
| `profile` | Background, experience, education, languages, qualifications, capabilities, aspirations, preferences and development |
| `projects` | Career-oriented accounts of undertakings, contributions, skills used, learning and links to actual work |
| `brand` | Positioning, audiences, messaging principles, design briefs and visual identity rules |
| `assets` | Reusable external-facing material, separated into drafts and approved staged versions, plus service/surface descriptions |
| `research` | Selected companies, opportunities, comparable professionals and resume references, with archival history |

These are user-record concepts, not required mirrors of installable skill groups. A workspace index maps them to canonical existing records. New work can adopt the reference names; existing notes need not move.

Profile and selected project evidence ground brand decisions and assets. Research informs market understanding, targeting, development and presentation without manufacturing facts about the user. Live external surfaces establish actual published state. Differences between live content and staged material are reconciled by the user, not resolved through automatic synchronization.

## User Stories

1. As a professional, I want all workspace records, including public-ready assets, to remain private so that preparation does not imply publication.
2. As a professional, I want local files, a Git repository or another Markdown-capable service to work so that storage does not determine the career model.
3. As an existing notes user, I want my current files mapped to the model so that adopting skills does not force migration.
4. As a new user, I want only the records needed for my current task created so that setup stays small.
5. As a user of one skill, I want it to work from supplied files or pasted material so that full setup and other installed skills are optional.
6. As an agent, I want a source map and task-specific contract so that I can identify relevant inputs and authorized output locations without reading the entire workspace.
7. As a professional, I want experience, education, languages and qualifications recorded so that career assets use a sufficiently complete background.
8. As a professional, I want strengths, skills and achievements linked to support so that claims remain defensible.
9. As a professional, I want my north star, motivations, values, interests and aspirations recorded separately from accomplishments so that intent does not become fabricated experience.
10. As a professional, I want preferences and practical constraints available so that growth and opportunity recommendations fit my circumstances.
11. As a professional, I want feasible development actions and evidence milestones so that learning connects to my chosen direction.
12. As a professional, I want progress reviews based on actual outcomes so that completing a course does not automatically establish competence.
13. As a project owner, I want one account of each relevant project so that its learning, contribution and work links are not copied across unrelated records.
14. As a professional, I want a project distinguished from supporting evidence so that merely starting an experiment does not prove a capability.
15. As a professional, I want brand guidance to identify positioning, audiences and messaging so that presentation has a coherent purpose.
16. As a professional, I want visual rules for typography, palette, logos and composition so that selected assets can be reused consistently.
17. As an employee, I want personal brand scoped to my own presence and career assets so that employer presentations are not automatically treated as personal branding.
18. As a professional, I want one reusable bio or headline where appropriate so that each surface does not acquire a competing master copy.
19. As a professional, I want intentional surface and resume adaptations so that one underlying record can support different recipients without unnecessary presentation variants.
20. As a professional, I want drafts distinct from approved staged material so that I know what is ready to use.
21. As a professional, I want meaningful asset versions and feedback preserved so that refinement does not overwrite alternatives or an approved identity.
22. As a professional, I want service records describing accounts, purposes and available read/update methods so that an agent knows where and how presentation exists externally.
23. As a professional, I want actual published content inspected where possible so that local approval is not mistaken for deployment.
24. As a professional, I want inaccessible surfaces and observation limitations reported so that an audit does not claim unseen content is aligned.
25. As a professional, I want to choose how differences between staged and live content are reconciled so that intentional public edits are not overwritten.
26. As a professional, I want factual inconsistencies flagged before importing public changes so that presentation does not silently override the career record.
27. As a design client, I want the agent to ask what I need and why before proposing assets or styles so that the current brief drives the work.
28. As a design client, I want guided discussion of usage, domain, audience and desired impression so that design decisions have a relevant basis.
29. As a design client, I want historical aesthetics reused only when I explicitly select them so that a past experiment does not become a permanent constraint.
30. As a design client, I want verbal concepts discussed before visual drafts so that I can choose an idea rather than reject arbitrary logos.
31. As a design client, I want simple, distinctive monochrome logo drafts and practical-size checks so that colour and effects do not disguise weak construction.
32. As a design client, I want typography-only, banner-only or other scoped work supported so that every request does not require a logo or complete identity kit.
33. As a professional, I want relevant public profiles, portfolios and resume examples researched so that I can understand the market and find inspiration.
34. As a professional, I want peers, aspirational examples and templates distinguished so that comparisons are contextual rather than false evidence of direct competition or hiring success.
35. As a professional, I want employer fit researched separately from current vacancies so that promising companies can remain targets without an opening today.
36. As a job seeker, I want role and company recommendations grounded in my work preferences, location, eligibility and other constraints so that apparent matches are practical.
37. As a research user, I want a shortlist before retention and the option to save some, all or none so that research stays intentional.
38. As a research user, I want one useful company, opportunity or comparator record with linked related records so that retained findings remain understandable without duplication.
39. As a research user, I want sources, dates, observations, unknowns and reasons for keeping a reference so that it remains useful later.
40. As a research user, I want resume links and useful notes rather than copies of other people's resumes so that my library stays focused on references.
41. As a research user, I want useful expired opportunities and older examples retained so that age alone does not erase market knowledge or inspiration.
42. As a research user, I want requested review and guided archiving so that research can be maintained without automatic deletion.
43. As a research user, I want agents to ask before acting on stale content encountered during unrelated work so that discovery does not initiate unrequested cleanup.
44. As a skill maintainer, I want concise Input / Scope / Output contracts so that responsibility and record ownership are clear without duplicating the workspace guide in every skill.

## Implementation Decisions

### Workspace, authority and terminology

- The five reference homes are profile, projects, brand, assets and research. Earlier suggestions using personal-projects, personal-brand, career-assets or publication as workspace home names are superseded. Installable skill categories are a separate organization and have not been renamed to match them.
- The whole workspace is private. Core profile covers both supported professional information and clearly distinguished aspirations; private garden refers to the workspace, not a separately public/private split inside it.
- Brand is the guidance layer, broader than design alone. Assets are the reusable outputs. Online presence is observable external presentation; reputation is how others perceive the person, supported imperfectly by attributed signals.
- One canonical record owns each fact, project account or reusable content item. Summaries and adaptations link to that authority rather than become independent competing records. User testimony may support a claim; external proof is not required for everything.
- A minimal index records authority mappings, storage root, write workflow, optional tracker and publication boundaries. Read relevant records incrementally. Fixed schemas, YAML, database fields and mandatory identifiers are not required.
- Project accounts capture purpose, status, contribution, skills, learning and potential presentation value; they link actual work rather than duplicate its repository or backlog.

### Asset lifecycle and public surfaces

- Drafts are proposals; staging contains the latest explicitly approved reusable material. No final directory is needed, and neither state proves publication. Approval of content does not authorize external publishing.
- Reuse common bios, headlines and visual masters. Add audience/surface-specific versions only for an intentional difference, such as a tailored resume or required crop.
- Service descriptions identify the service/account, URL or source location, intended use, related staged assets, available inspection/update methods, limitations and permissions. Begin with a compact record and split it if needed.
- Underlying facts and intentions remain authoritative in the workspace; an external surface is authoritative about what is actually published there. Website source code alone does not establish what is deployed.
- Inspection can use available connectors, APIs, accessible pages or supplied exports/text. Record what was inspected and when. A stored last-observed publication baseline is not required; missing history must not lead to guesses about which side changed.
- Show discrepancies and ask whether to update the workspace, the external surface or retain a legitimate difference. Surface edits can inform workspace wording, but factual incoherence must be raised before importing claims.

### Research lifecycle

- Research includes employers, specific opportunities and comparable professionals, portfolios and resumes. The same benchmark capability can collect selected examples and compare them; a separate collection-only skill was not approved.
- Present a shortlist before persistence. Save the user's selections, including all when selected, or a set covered by an explicit save instruction. A user-supplied reference may also be retained when requested.
- Retain useful linked findings and why they matter, not every retrieved page, query or intermediate thought. Comparator resumes remain links, not downloaded files. Related opportunity/company records link instead of repeating company descriptions.
- Separate observed facts, inferred fit and unknowns. Company suitability is independent of vacancy availability; verified openings need current original employer or authorized recruiting evidence. Remote location, languages, compensation and eligibility must not be invented from silence.
- Research is for future reference, market understanding and inspiration for development or presentation. Another person's experience or a vacancy requirement never establishes a fact about the user.
- Research review is on request, archive-first and based on usefulness rather than age alone. An agent may archive under explicit selection or established guidance; ambiguous cases prompt the user. Deletion remains manual. Incidental stale-content discovery prompts an offer to review, not silent action or background maintenance.

### Skill responsibilities and packaging

- Preserve independently usable skills grouped by career activity: career-direction, career-evidence, career-development, personal-brand and job-hunt, with setup cross-cutting. Group folders are not orchestrators or a mandatory execution chain.
- Split design discovery, creation and review. Discovery uses a design-focused interview without requiring grill-me; creation owns concept research/selection, drafts, refinement and production self-checks; review provides critique without modifying assets or implying approval.
- Discovery asks high-level need and purpose first, then unresolved usage, audience, domain, intended impression, personality, scope and constraints. Do not assume a tech or geometric aesthetic, keep an old font, or propose continuation from memory without an explicit current reference. A link to the skill is not a design reference.
- Explore a small relevant online reference set when possible and explain inspiration without copying. Discuss distinct verbal concepts before drafting; an explicitly selected current concept can satisfy that step. Research availability and visual verification limits remain explicit.
- Logos use one clear idea, few elements, a recognizable silhouette and monochrome/reversal checks. Inspect actual required sizes, geometry and exports when tools permit. Do not rely on effects, claim trademark clearance or label unverified work final.
- Preserve option/revision IDs, selected feedback and exact approval status. Full exports belong to selected versions, not every exploratory option. Produce only scoped assets; typography/composition and banner work can proceed without a logo.
- Personal-brand work supplies positioning and selected reusable messaging; maintain-profile reconciles personal facts; development skills plan/review growth; company/job search researches opportunities; benchmarking adds external comparisons; audits inspect facts and presentation against current authorities. Review-research owns requested archival maintenance.
- Each skill has a lightweight Markdown Input / Scope / Output contract identifying relevant records, a meaningful boundary and a reviewable result/default destination. Default paths resolve through the workspace map; full workspace notes are not repeated in every skill. No formal runtime contract schema is required.
- Keep instructions concise and self-contained, with progressive disclosure for needed references, a small file tree and full exports only when relevant. Keep task-oriented invocation names unless a separate rename is approved. Potential names such as define-brand remain proposals, not settled changes.

## Testing Decisions

- Prefer the existing highest-level seam: realistic user requests evaluated through the skill's observable response, authorized record changes and resulting artifacts. Do not prove behavior by matching exact phrasing or contract headings.
- Reuse the existing documented behavioral scenarios for setup, reflection, factual reconciliation, development, design, benchmarking, employer/job search, audits and research review. The scenario collection is not itself an executed benchmark.
- Cover existing-layout mapping and local-only input without mandatory migration, provider integration, unused directories or full setup. Check source authority and privacy boundaries as well as successful saves.
- Exercise ask-first design with historical geometric/font preferences present but not selected, explicit-reference continuation, concept selection before drafts, scoped non-logo work, preserved alternatives and truthful verification limits.
- Exercise approved-but-unpublished assets, intentional surface adaptations, inaccessible services and unexplained live/staged discrepancies. Expect a reconciliation choice rather than automatic overwrite or inferred change direction.
- Exercise shortlist selection, retained resume links, useful expired references and guided archiving. Verify that incidental stale findings do not cause unrequested maintenance and no automatic deletion occurs.
- Exercise company geography/remote constraints and vacancy verification separately from inferred employer fit. Exercise comparator evidence without invented personal skills, metrics or hiring outcomes.
- Keep structural packaging/frontmatter validation and Markdown link checks as separate checks. They do not prove behavioral correctness. Existing isolated setup/discovery checks provide limited evidence, not full cross-harness coverage.
- This spec reuses the testing boundaries already discussed. No new provider integration or automated behavioral harness is committed by the spec.

## Out of Scope

- Migrating or renaming actual user notes without a separate instruction; examples from an existing private workspace are not mandatory schemas.
- Public publishing, job applications, employer outreach, purchases, training enrollment or external mutations merely because a skill can prepare material.
- Automatically installing or updating skills already installed in ChatGPT or another harness.
- Building service-specific APIs, scraping scripts, connectors, automatic synchronization or scheduled maintenance now. Feasibility must be researched separately for each service.
- Mandatory publication snapshots, a final directory, a copy of every online page, copied third-party resume files, or indiscriminate search-result retention.
- General company branding, product UX, compulsory employer-presentation branding, a database-backed career product or a mandatory design-token system.
- Automatic research deletion, automatic factual acceptance of imported public claims, invented achievements or a guarantee that a design is unique or legally cleared.
- Unapproved skill/package renames or a new separate skill solely to collect comparator profiles.

## Further Notes

- The operational workspace guide is [WORKSPACE.md](WORKSPACE.md); terms are defined in the [glossary](../GLOSSARY.md), and package responsibilities are summarized in [ARCHITECTURE.md](ARCHITECTURE.md). This specification preserves the decision rationale and scope rather than replacing those operating documents.
- The interview's five skill domains describe activities; the final five workspace homes describe user records. Conflating them was an earlier proposal and is superseded.
- Earlier suggestions to keep output assets inside brand guidance, require a final directory, retain a publication baseline or automatically archive old content were rejected. Brand guidance, reusable assets and actual external publication have separate roles.
- Surface automation remains desirable but uncommitted. The model accepts whatever inspection method is available without promising API access, deployment visibility or automatic public-profile extraction.
- Current PR implementation and validations are evidence to assess against this spec, not proof that every story has shipped. Remaining naming proposals and future integrations require separate decisions.
- Synthesized using [Matt Pocock's to-spec skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/to-spec). The user's requested destination is this pull request, rather than a separate issue; no issue or triage label is required for this delivery.
