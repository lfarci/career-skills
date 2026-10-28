---
name: ask-career-skills
description: Help me choose which Career Skills workflow to use next.
disable-model-invocation: true
---

# Ask Career Skills

Recommend a next step in Career Skills. This is a **manual navigation skill**, not a required orchestrator. Users can run any other skill directly, with or without setup.

## Contract
- **Input:** The user's current goal, prior actions and any available workspace index or supplied context.
- **Scope:** Choose an appropriate next task and skill. Do not execute other skills, edit records or start a sequence.
- **Output:** One primary skill recommendation with a reason and ready-to-use request; up to two distinct alternatives if helpful.

## Steps

1. Identify the user's immediate goal and last completed task from the conversation. Check a workspace index or existing records **only when needed** to avoid recommending already-completed work. Work without setup or workspace access; use stated assumptions instead of making the user repeat answers.
2. Route by the **outcome**, not by a fixed sequence:
   - Initialize a clean standardized `career/` or discover prior documents to import: `setup-career-skills`; explicitly align/migrate an occupied legacy workspace or repair broken paths: `validate-workspace` (if installed); changed career facts: `maintain-profile`; uncertain direction: `reflect`.
   - Career growth: `plan-development` for a plan or `review-progress` for an existing one.
   - Positioning: `personal-brand`; inspect one surface: `audit-surface`; reconcile multiple surfaces: `audit`.
   - Visual identity: `define-design-brief` for discovery, `create-design-assets` for production, `review-design` for critique.
   - Opportunities: `find-companies` for target employers, `find-jobs` for live vacancies, `build-resume` for application documents.
   - Examples and retained research: `benchmark-profile` for public examples, `review-research` for user-guided maintenance.
3. Recommend the most useful **next action**, why it fits, the input it needs and a concrete invocation example. When the user explicitly names a goal, route there without forcing prerequisites. When the goal is open-ended, suggest addressing unreliable facts first, then unclear direction, then the user's preferred branch; show at most two meaningful alternatives.
4. A missing installed skill is an option to install, not an action already performed. If no career skill is relevant, say so. Ask one concise question only if selecting a useful next step truly depends on an unanswered preference.

## Done when

- The user has a clear, evidence-grounded next action and the matching skill name or an explicit no-skill recommendation.
- Already completed work is respected; setup, profile maintenance and reflection are suggested only when useful.
- No other skill, tool workflow, file mutation or recurring process was triggered by this routing session.
