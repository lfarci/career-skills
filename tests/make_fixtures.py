"""Regenerate tests/fixtures/ (synthetic data only). Run: python3 tests/make_fixtures.py"""
import json, shutil
from pathlib import Path
F = Path(__file__).resolve().parent / "fixtures"
KEEP = F / "setup-pdf-linkedin-conflicts" / "sources"  # committed binary sources (synthetic PDF and zip)
for d in (F.iterdir() if F.exists() else []):
    if d.is_dir() and d != KEEP.parent:
        shutil.rmtree(d)
def w(case, rel, text):
    p = F / case / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text.strip() + "\n", encoding="utf-8")

EXP = """# Experience
## Software Engineer (Consultant), Contoso Consulting
- Dates: Mar 2021 – present
- Location: Brussels
- Assignment: Fabrikam Bank, payment API migration to .NET 8 (2022–2024), team of 6.
- Assignment: Northwind Retail, React dashboard for store managers (2021–2022).
- Source: old-notes/resume.md
## Software Engineering Intern, Tailspin Labs
- Dates: Feb 2020 – Jul 2020
"""
def base(case, readme_records=None, status="ready", extra_readme=""):
    recs = readme_records or [("Contact","profile/contact.md"),("Experience","profile/experience.md"),("Skills","profile/skills.md"),("Education","profile/education.md"),
            ("Qualifications","profile/qualifications.md"),("Direction","profile/direction.md"),("Positioning","brand/positioning.md"),
            ("Project: Contoso AI assistant","projects/contoso-ai-assistant.md")]
    links = "\n".join(f"- [{t}]({p})" for t,p in recs)
    w(case,"career/README.md",f"""# Career workspace

Storage: private local folder (Markdown)
Write policy: propose changes; direct edits only when approved
Publication: separate approval required

## Records
{links}

## Source inventory
| Source | Decision | Destination | Notes |
|---|---|---|---|
| old-notes/resume.md | imported | profile/experience.md | 2026-09 |

## Setup progress
Status: {status}
{extra_readme}""")
    w(case,"career/profile/experience.md",EXP)
    w(case,"career/profile/skills.md","# Skills\n- C#, .NET 8, SQL, TypeScript, React\n- Azure App Service, Azure Functions, Azure DevOps pipelines (application deployment)\n- Source: old-notes/resume.md")
    w(case,"career/profile/contact.md","# Contact (imported with approval)\n- Name: Alex Testa\n- E-mail: alex.testa@example.invalid\n- City: Brussels, Belgium")
    w(case,"career/profile/education.md","# Education\n- MSc Computer Science, Université Exemple, 2020")
    w(case,"career/profile/qualifications.md","# Qualifications\n- AZ-204 Azure Developer Associate, passed 2023 (credential ID on file)")
    w(case,"career/profile/direction.md","# Direction\n- Goal: grow toward solution architecture while staying hands-on.")
    w(case,"career/brand/positioning.md","# Positioning\n- Headline: .NET & Azure Engineer · Consulting\n- Audience: hiring managers at Benelux product companies")
    w(case,"career/projects/contoso-ai-assistant.md","# Contoso AI assistant\n- Status: experimental internal prototype (not in production)\n- Contribution: built the retrieval API in C#\n- Source: old-notes/projects.md")

# --- per case ---
base("profile-conflicting-credential")
w("profile-conflicting-credential","notes/2026-03-plans.md","# Plans\n- I plan to take certification X (AZ-305) in June 2026.")
w("profile-conflicting-credential","notes/2026-07-update.md","# Update\n- Passed certification X (AZ-305)!")
w("profile-conflicting-credential","notes/exam-receipt.txt","Pearson VUE (synthetic)\nExam: AZ-305\nStatus: SCHEDULED\nDate: 2026-11-20\n")

base("resume-unsupported-metrics")
w("resume-unsupported-metrics","job-ad.md","# Cloud Engineer, Woodgrove (synthetic)\nRequirements:\n- Kubernetes cluster administration (AKS), upgrades and node pools\n- Terraform\n- CI/CD for application deployment\n- Azure")

base("surface-inaccessible")

base("brand-private-boundary")
w("brand-private-boundary","career/profile/direction.md","# Direction (private)\n- Doubts: not sure I want to manage people; worried about losing hands-on work.\n- Goal: solution architecture.")
w("brand-private-boundary","career/profile/development.md","# Development (private)\n- Action plan: ask manager for an architecture-lead assignment by Q1 (internal).\n- Planned: AI-102 Azure AI Engineer certification (not taken yet).")
w("brand-private-boundary","career/brand/bio.md","# Public bio (current)\nSoftware engineer at Contoso Consulting.")

svg = lambda label,fill: f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" fill="{fill}"/><text x="100" y="115" font-size="48" text-anchor="middle" fill="#fff">{label}</text></svg>'
for c in ("identity-preserve-options-and-revisions",):
    base(c, extra_readme="- [Visual identity](brand/identity.md)")
    for n,f in (("a","#1D4ED8"),("b","#0F766E"),("c","#7C3AED")):
        w(c,f"career/assets/drafts/logo/{n}-v1.svg",svg("AT "+n.upper(),f))
    w(c,"career/assets/staged/logo/legacy-v3.svg",svg("AT","#111827"))
    w(c,"career/brand/identity.md","# Visual identity\nStatus: approved legacy-v3 (2025)\n- Logo: [legacy v3](../assets/staged/logo/legacy-v3.svg)\n\n## New identity (in progress)\nStatus: pending\n- Concepts: [A/v1](../assets/drafts/logo/a-v1.svg), [B/v1](../assets/drafts/logo/b-v1.svg), [C/v1](../assets/drafts/logo/c-v1.svg)")

c="workspace-map-existing"
w(c,"notes/profile/goals.md","# Goals\n- Become a platform engineer within 2 years.")
w(c,"notes/profile/experience.md",EXP.replace("Source: old-notes/resume.md",""))
w(c,"notes/personal-projects/home-lab.md","# Home lab\n- Kubernetes (k3s) cluster on 3 Raspberry Pis, GitOps with Flux.")
w(c,"notes/personal-brand/bio.md","# Bio\n.NET & Azure engineer who likes platform work.")

base("audit-drift")
w("audit-drift","surfaces/resume.md","# Alex Testa\n- Built the Contoso AI assistant, running in production for 2,000 users.")
w("audit-drift","surfaces/homepage.html","<html><body><h1>Alex Testa</h1><p>I built Contoso's AI assistant, now in production.</p></body></html>")
w("audit-drift","surfaces/linkedin/Profile.csv","First Name,Last Name,Headline,Summary\nAlex,Testa,.NET & Azure Engineer,\"Shipped an AI assistant to production at Contoso.\"")

w("profile-no-intent-existing","notes/career-notes.md","# Career notes\n"+EXP)

base("workspace-stale-index", readme_records=[("Experience","profile/experience.md"),("Skills","profile/skills-old.md"),("Education","profile/education.md"),("Qualifications","profile/qualifications.md"),("Direction","profile/direction.md"),("Positioning","brand/positioning.md"),("Project: Contoso AI assistant","projects/contoso-ai-assistant.md")])

c="workspace-valid-custom-layout"
base(c, readme_records=[("Experience","profile/experience.md"),("Skills","profile/skills.md"),("Education","profile/education.md"),("Qualifications","profile/qualifications.md"),("Direction","profile/direction.md"),("Positioning","personal-brand/positioning.md"),("Project: Contoso AI assistant","projects/contoso-ai-assistant.md")])
(F/c/"career/brand/positioning.md").rename(F/c/"career/brand/x"); (F/c/"career/personal-brand").mkdir(); (F/c/"career/brand/x").rename(F/c/"career/personal-brand/positioning.md"); (F/c/"career/brand").rmdir()

c="workspace-full-review-request"
base(c, readme_records=[("Experience","profile/experience.md"),("Skills","profile/skills.md"),("Education","profile/education.md"),("Qualifications","profile/certs.md"),("Direction","profile/direction.md"),("Positioning","brand/positioning.md")])
w(c,"career/assets/drafts/resumes/general/resume.md","# Resume draft\nSee [experience](../../../../profile/experiance.md).")

base("workspace-user-goal-first")
base("ask-career-skills-after-setup")
base("ask-career-skills-structure", readme_records=[("Experience","profiles/experience.md"),("Skills","profile/skills.md"),("Education","profile/education.md"),("Qualifications","profile/qualifications.md"),("Direction","profile/direction.md"),("Positioning","brand/positioning.md"),("Project: Contoso AI assistant","projects/contoso-ai-assistant.md")])

c="setup-fresh-selective-import"
w(c,"old/resume.md","# Alex Testa — Resume\n"+EXP)
w(c,"old/profile-notes.md","# Notes\n- Languages: French (native), English (C1)\n- Hobbies: climbing")
for n,t in (("payments-api","Payment API migration (Fabrikam Bank)"),("store-dashboard","Store manager dashboard (Northwind)"),("ai-assistant","Contoso AI assistant prototype")):
    w(c,f"old/projects/{n}.md",f"# {t}\n- Role: developer\n- Stack: .NET / React")

c="workspace-migrate-standard-homes"
w(c,"career/README.md","# Career workspace\n\n## Records\n- [Experience](profile/experience.md)\n- [Bio](personal-brand/bio.md)\n- [Home lab](personal-projects/home-lab.md)\n- [Services](services.md)\n")
w(c,"career/profile/experience.md",EXP)
w(c,"career/personal-brand/bio.md","# Bio\nSee [home lab](../personal-projects/home-lab.md).")
w(c,"career/personal-projects/home-lab.md","# Home lab\n- k3s cluster, GitOps.")
w(c,"career/services.md","# Services I offer\n- Freelance .NET code reviews")

c="setup-role-history-with-internships"
w(c,"sources/resume.md","""# Sam Example — Resume (synthetic)
## Senior Consultant, Contoso Consulting (Jan 2024 – present)
## Consultant, Contoso Consulting (Sep 2021 – Dec 2023)
## Junior Consultant, Contoso Consulting (Sep 2019 – Aug 2021)
### Engagement: Fabrikam Bank cloud migration (Mar 2022 – Jun 2024, spans Consultant and Senior Consultant)
- Moved 40 services to Azure; led the networking workstream from 2024.
## Intern, Tailspin Labs (Feb – Jun 2019)
## Intern, Litware (Jul – Aug 2018)
""")
w(c,"sources/older-notes.md","# Older notes\n- At Litware I wrote Python data scripts.\n- Promotion to Senior Consultant came with team-lead duties for 3 people.")

c="setup-first-batch-does-not-end-intake"
w(c,"career/README.md","# Career workspace\n\nWrite policy: direct edits approved\n\n## Records\n- [Experience](profile/experience.md)\n- [Skills](profile/skills.md)\n- [Certifications](profile/certifications.md)\n\n## Source inventory\n| Source | Decision | Destination |\n|---|---|---|\n| sources/resume.md | imported | profile/experience.md, profile/skills.md, profile/certifications.md |\n| sources/leadership-and-projects.md | pending | |\n| sources/education-and-languages.md | pending | |\n| sources/side-projects.md | pending | |\n\n## Setup progress\nStatus: in progress")
w(c,"career/profile/experience.md",EXP)
w(c,"career/profile/skills.md","# Skills\n- C#, Azure")
w(c,"career/profile/certifications.md","# Certifications\n- AZ-204 (2023)")
w(c,"sources/resume.md","# Resume\n"+EXP)
w(c,"sources/leadership-and-projects.md","# Leadership and projects\n- Led a 3-person team on the Fabrikam payment API (2023–2024).")
w(c,"sources/education-and-languages.md","# Education\n- MSc Computer Science, 2020\n# Languages\n- French, English")
w(c,"sources/side-projects.md","# Side projects\n- Open-source Blazor component library (120 stars).")

c="setup-resume-invalid-workspace-before-import"
base(c, status="in progress", extra_readme="Next: import projects from sources/projects/")
(F/c/"career/profile/experience.md").rename(F/c/"career/profile/work-history.md")
w(c,"sources/projects/payments-api.md","# Payment API migration\n- .NET 8, 2022–2024")

c="setup-resume-valid-continue-next-step"
base(c, status="paused", extra_readme="Source review: completed\nNext decision: select project evidence (candidates: sources/projects/payments-api.md, sources/projects/store-dashboard.md)")
w(c,"sources/projects/payments-api.md","# Payment API migration\n- .NET 8, 2022–2024")
w(c,"sources/projects/store-dashboard.md","# Store dashboard\n- React, 2021–2022")

c="setup-named-folder-is-root"
w(c,"notes/cv.md","# CV (approved for import: initial role summary)\n"+EXP)
w(c,"notes/todo.md","# Todo\n- buy milk")

c="setup-consolidation-is-not-lossless"
for i in range(1,35):
    extra = "\n- Detail: certificate PDF and grade transcript attached here." if i in (7,19,28) else ""
    w(c,f"career/note-{i:02d}.md",f"# Old note {i}\n- Fact {i}: synthetic career detail {i}.{extra}")
links=[]
for i in range(1,22):
    srcs=" ".join(f"[note-{j:02d}](../career/note-{j:02d}.md)" for j in ((i*34)//21-1, (i*34)//21) if 1<=j<=34 and j not in (7,19,28))
    w(c,f"career-new/profile/record-{i:02d}.md",f"# Record {i}\n- Summary of old notes. Evidence: {srcs}")
    links.append(f"- [Record {i}](profile/record-{i:02d}.md)")
w(c,"career-new/README.md","# Career workspace (new)\n\n## Records\n"+"\n".join(links))

c="setup-cutover-checks-inbound-links"
w(c,"backup/career/personal-brand/bio.md","# Bio (old)")
w(c,"backup/career/personal-projects/home-lab.md","# Home lab (old)")
for i in range(1,22):
    w(c,f"career/profile/record-{i:02d}.md",f"# Record {i}")
w(c,"career/README.md","# Career workspace\n\n## Records\n"+"\n".join(f"- [Record {i}](profile/record-{i:02d}.md)" for i in range(1,22))+"\n\n## Setup progress\nStatus: cutover pending")
w(c,"blog/2025-talk.md","# My talk\nBio: [bio](../career/personal-brand/bio.md)\nDemo: [home lab](../career/personal-projects/home-lab.md)")
w(c,"README.md","# Notes repo\n- [Career brand](career/personal-brand/bio.md)")

c="setup-index-holds-no-facts"
w(c,"old-notes/resume.md","# Resume\n"+EXP+"\n## Education\n- MSc Computer Science, Université Exemple, 2020\n## Skills\n- C#, Azure, React\n## Certification\n- AZ-204 (2023)")
w(c,"old-notes/goals.txt","Goal: solution architect in 3 years.")
w(c,"old-notes/side-project.md","# Side project\n- Blazor component library, open source.")

c="setup-resume-facts-in-index-asks-first"
w(c,"career/README.md","# Career workspace\n\n## Records\n- [Experience](profile/experience.md)\n\n## Captured facts\n- Education: MSc Computer Science, 2020\n- Skills: C#, Azure, React\n- Certifications: AZ-204 (2023)\n- Goals: solution architect\n\n## Setup progress\nStatus: in progress")
w(c,"career/profile/experience.md",EXP)

c="repair-renamed-record-same-fix"
base(c); (F/c/"career/profile/skills.md").rename(F/c/"career/profile/technical-skills.md")

c="design-banner-concepts-after-logo-approved"
base(c, extra_readme="- [Visual identity](brand/identity.md)")
w(c,"career/assets/staged/logo/a-v2.svg",svg("AT","#1D4ED8"))
w(c,"career/brand/discovery.md","# Design brief\n- Deliverables: logo (done), LinkedIn banner (next)\n- Mood: calm, technical, Brussels")
w(c,"career/brand/identity.md","# Visual identity\nStatus: approved a-v2 (logo only)\n- Logo: [A/v2](../assets/staged/logo/a-v2.svg)\n- Banner: not started")

c="setup-pdf-linkedin-conflicts"
for n in ("resume-2025.pdf","linkedin-export.zip"):
    assert (F/c/"sources"/n).is_file(), f"committed binary fixture missing: {n}"

c="design-approve-stages-exact-version"
base(c, extra_readme="- [Visual identity](brand/identity.md)")
for n,f in (("a","#1D4ED8"),("b","#0F766E")):
    w(c,f"career/assets/drafts/logo/{n}-v1.svg",svg("AT "+n.upper(),f))
w(c,"career/assets/drafts/logo/a-v2.svg",svg("AT A2","#1E40AF"))
w(c,"career/brand/identity.md","# Visual identity\nStatus: pending\n- Concepts: [A/v1](../assets/drafts/logo/a-v1.svg), [A/v2](../assets/drafts/logo/a-v2.svg), [B/v1](../assets/drafts/logo/b-v1.svg)")

base("workspace-healthy-resume-no-helper")
print(sorted(p.name for p in F.iterdir()))
