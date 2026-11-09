# Profile layers and optional headings

`profile/` has three layers:

- `facts/`: what happened and can be checked.
- `criteria/`: what a role must offer now.
- `goals/`: aspirations and development.

maintain-profile writes `facts/`, and records `criteria/` only as the user states them. `goals/` belongs to reflect and plan-development.

The headings below are optional. Use them when they help, keep the user's wording, and leave a `TODO` where the source is silent. Never invent a metric, level or ranking.

## facts/experience.md, per role

Position · Organisation · Start / end (`YYYY-MM`, approximations marked) · Location · Summary · Highlights (each linked to a project record or evidence) · Responsibility level (optional, self-assessed by the user on the SFIA 1–7 scale: Follow, Assist, Apply, Enable, Ensure/advise, Initiate/influence, Set strategy/inspire/mobilise).

Presentation advice (how to phrase a role on a resume) belongs in `brand/`, not here.

## facts/qualifications.md and skills.md

- **Credential:** name · issuer · date · URL or ID · current or historical.
- **Skill:** name · level · keywords · evidence link.

## facts/achievements.md: dated brag log

One dated entry per achievement or piece of feedback, newest first:

```markdown
### YYYY-MM: short title
- What: contribution and impact (only what the source supports)
- Kind: project / collaboration & mentorship / design & documentation / company building / learning / feedback received
- Dimension: Technology / System / People / Process / Influence (optional)
- Evidence: link to project record, review, message or artefact
```

## facts/stories.md: STAR stories

```markdown
### Story title
- Situation:
- Task:
- Action: what I did (not the team)
- Result: outcome, measured only where a source supports it
- Shows: skills or dimension
- Evidence: link
- Date:
```

## facts/compensation.md

The current package: a private baseline with source and date, never a target. A package overview with the same fields for the current job, the expectations and each offer makes comparisons line by line. Keep only the fields that apply in the user's country, and write `TODO` for unknown values:

- Employer: name, sector, size, multinational.
- Contract: title, seniority, contract type, official and real hours per week, on-call duty, vacation days.
- Salary: gross and net per month, number of monthly payments (13th month, holiday pay), expense allowances, bonus or incentive plans and their targets, equity.
- Benefits: company car or mobility budget (with personal contribution and fuel or charging card), meal vouchers, eco vouchers, group insurance or pension (employee and employer %), health and other insurance, phone, internet, home-working allowance, training budget.
- Mobility: work location, distance and commute, travel compensation, telework days.
- Other: ease of taking leave, stress, people managed.

Belgian users can follow the r/BESalary template (https://www.reddit.com/r/BESalary/comments/12xam5d/whats_your_wage_and_work_conditions_template/).

## criteria/

- `conditions.md`: location, work mode, travel, commute, contract type, languages, notice period.
- `salary-expectations.md`: what a next role must pay and offer: minimum and target gross and net, must-have benefits, acceptable trade-offs. Use the same package fields as `facts/compensation.md` so an offer compares line by line with both; write `TODO` until the user sets a value, never a computed target.
- `expectations.md`: Must-haves, Nice-to-haves, Deal-breakers. Optionally group them by work value (Achievement, Independence, Recognition, Relationships, Support, Working Conditions). End with a short screening checklist.
