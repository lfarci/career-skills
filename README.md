# Career Skills

Career Skills turns your AI coding agent into a career assistant. It builds and maintains a **private career workspace** in a folder you own: your profile (roles, skills, projects), your personal brand, your visual identity, tailored resumes and a job search. Everything is plain Markdown, and **nothing is published, sent or applied for without your approval**.

## Install

You need [Node.js](https://nodejs.org/) (for `npx`) and Python 3 (on Windows the command is `py`). Create a private folder, then run the line for your agent inside it:

```bash
mkdir my-career && cd my-career && git init
```

| Agent | Install | Skills folder | Start |
| --- | --- | --- | --- |
| GitHub Copilot (CLI and VS Code) | `npx skills add lfarci/career-skills --skill '*' -y --copy -a github-copilot` | `.agents/skills/` | `copilot`, or open the folder in VS Code and use Copilot Chat in Agent mode |
| Claude Code | `npx skills add lfarci/career-skills --skill '*' -y --copy -a claude-code` | `.claude/skills/` | `claude` |
| Codex | `npx skills add lfarci/career-skills --skill '*' -y --copy -a codex` | `.agents/skills/` | `codex` |
| OpenCode | `npx skills add lfarci/career-skills --skill '*' -y --copy -a opencode` | `.agents/skills/` | `opencode` |

To update later: `npx skills update -y`.

## Getting started

1. **Add your material.** Put old CVs, your LinkedIn data export (zip), notes or portfolio pages in `inbox/` inside your folder. They are only read when you say so.
2. **Run setup.** Start your agent in the folder and type:

   > Use the setup-career-skills skill. Create my private career workspace in ./career. My material is in ./inbox; you may read it and write records. Start with my role history.

   Setup reads your sources, asks about anything unclear or conflicting, and writes `career/README.md` (an index with your progress) plus records such as `career/profile/experience.md`. Private details (health, salary, family) are left out unless you ask. This one clean, verified record of your career is what every other skill builds on, so resumes and profiles stay truthful and consistent.
3. **Take breaks.** Stop at any time; later say *"Resume my setup"* and it continues where you left off.
4. **Check the workspace** (use `.claude/skills/...` instead of `.agents/skills/...` for Claude Code):

   ```bash
   python3 .agents/skills/setup-career-skills/scripts/check_workspace.py career   # macOS / Linux
   py .agents\skills\setup-career-skills\scripts\check_workspace.py career        # Windows
   ```

   It prints `Status: usable`, or `needs repair` with each broken link.

## What next

Just ask in plain language, for example:

- *"Use the personal-brand skill. Help me choose how to present myself and draft my LinkedIn headline and About."*
- *"Use the visual-identity skill. Create a simple colour palette, fonts and a banner for my brand."*
- *"Use the build-resume skill for this job ad: …"*
- *"Find remote .NET jobs that match my profile."*
- *"Use the ask-career-skills skill. What should I do next?"*

See [all skills and what they do](docs/SKILLS.md).

## Contributing

Read [AGENTS.md](AGENTS.md), the [architecture](docs/ARCHITECTURE.md), [workspace model](docs/WORKSPACE.md) and [evaluation guide](docs/EVALUATION.md). MIT [license](LICENSE).
