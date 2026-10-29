---
name: audit
description: Audit one or several professional surfaces (resume, LinkedIn, GitHub, portfolio, website) against career facts and brand guidance. Use for checking a profile's claims, consistency or visual drift.
---

# Audit Professional Surfaces

Check what a surface actually shows against the user's canonical facts and approved brand guidance. One surface gets a findings report; several surfaces also get a cross-surface matrix that finds *relationships*, not concatenated reports. This is not an SEO, accessibility, performance or security audit.

## Contract
- **Input:** One or more surfaces from brand/surfaces.md or supplied directly (URL, export or pasted text), plus relevant profile/ facts, brand/positioning.md, brand/identity.md and staged assets.
- **Scope:** Find factual, presentation and visual-drift issues; ask how to reconcile differences instead of assuming live or staged content is right. Never edit surfaces or overwrite records.
- **Output:** Findings in the response or the user's existing review/tracker record; with several surfaces, a discrepancy matrix and deduplicated actions.

## Steps
1. **Scope.** Identify each surface, accessible version, date checked and audience. Mark inaccessible parts unknown; accept exports and pasted content. In an export archive (for example a LinkedIn data zip) read only the profile files the audit needs, in place; leave messages and connections unopened.
2. **Extract claims** by subject: headline, roles and dates, experience, skills, credentials, projects, links, contact. When visible, note banner, avatar/logo, palette and typography.
3. **Compare with canonical records.** Classify each difference as **confirmed mismatch**, **needs verification**, **valid tailoring** or **stylistic opportunity**. Compare text with the staged copy and the surface's `Emphasise:` line, and visuals with brand/identity.md when it exists; platform crops and font fallbacks are not drift.
4. **Several surfaces only:** build an alignment matrix (canonical value, each surface's wording or omission, classification), add a visual-identity row when relevant, and check real links between surfaces (site → resume, GitHub → portfolio). Trace root causes and fix source facts before derived copies.
5. **Credential surfaces** (Credly, Microsoft Learn transcript, similar): a certification or badge that is missing or outdated in profile/qualifications.md becomes a proposed profile update (name, issuer, date, evidence URL). Ask the user; apply only an approved change, following maintain-profile's record rules. A recurring check is the host's scheduling, not this skill.
6. **Report.** Prioritize by risk. For each actionable item give surface(s), current state, evidence, desired outcome and a verifiable acceptance criterion. Check the tracker for existing issues before proposing new ones; write to a tracker only when authorized, otherwise output issue-ready Markdown.

## Done when
- Every accessible in-scope surface was inspected; inaccessible content is reported unknown, not assumed aligned.
- Confirmed contradictions cite evidence; tailoring and platform variants are not flagged as errors.
- Planned content is not treated as live.
- Every high-priority finding has a measurable correction; no duplicate items.
- Credentials found only on a surface are proposed as profile updates, never written silently.
- Nothing was published or written to a tracker without authorization.
