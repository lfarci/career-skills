# Manual setup scenarios for small models

## Reproduction

Use a fresh disposable directory and OpenCode session for each scenario. From the repository root, stage the skill and references with:

```sh
test_root=$(mktemp -d /tmp/setup-career-skills.XXXXXX)
mkdir -p "$test_root/.agents/skills"
cp -a skills/setup-career-skills "$test_root/.agents/skills/"
```

Run each exact prompt below from `$test_root` with:

```sh
opencode run --standalone --format json --model openrouter/openai/gpt-5.4-nano --title "<scenario>" "<prompt>"
```

The skill must appear in OpenCode's available skill list and the transcript must show a native `skill` call for `setup-career-skills`. Keep the session ID and output. For scenario 3, create the specified fictional README and role record inside its selected root before starting OpenCode. Do not use real career records.

Score observed behavior, not the agent's claims. Require a successful `skill` tool call for `setup-career-skills`, successful write results for expected files, and a later read/listing that verifies them. A missing native skill call, failed write, or claimed file absent from disk is a fail. In non-interactive `opencode run`, a `question` tool can report that it cannot wait for input; score the final response and ensure no dependent writes happen.

## 1. Named folder and supplied role

Prompt:

> Use setup-career-skills to create a workspace in a new folder named `career-skill-smoke` here.
>
> You can write local files.
>
> For now, use only this fictional career information:
>
> I worked at ExampleCo as a Software Engineer from January 2024 to December 2025.
>
> Start the setup.

Pass when `career-skill-smoke/` itself contains `README.md` and `profile/experience.md`, no `career-skill-smoke/career/` exists, the record contains only the supplied role and dates, and the README saves status, captured/deferred information, and one next decision. It must not ask to reconfirm the folder or local write permission already provided.

## 2. Missing destination

Prompt:

> Use setup-career-skills to start my private career workspace.

Pass when the first response asks one concise question about the destination. Before the user answers, there are no file reads outside the skill bundle, no career-source scans, and no workspace writes. In non-interactive mode, a textual request for the destination is acceptable if the question tool cannot wait for input.

## 3. Resume from a saved decision

Seed only fictional files under `career-skill-resume/`: a README with status `in progress`, one existing ExampleCo role record, and next decision `choose one priority direction for the next review`. Then prompt:

> Use setup-career-skills to resume `career-skill-resume` here. Continue from its saved next decision.

Pass when OpenCode reads only the named workspace's README and mapped role record, keeps the named folder as root, does not duplicate or rewrite the role, and asks one focused question about the saved priority decision. It must not restart location intake or claim setup is complete.

## Recorded manual run

On 2026-10-29, the revised skill passed all three scenarios in real OpenCode sessions on `openrouter/openai/gpt-5.4-nano`:

| Scenario | Session | Result |
| --- | --- | --- |
| 1. Named folder and role | `ses_e7952d6c8ffe9ABiZQZlfI8HEG` | Pass: native skill call; wrote and reread the named root's README and ExampleCo role; no nested `career/`; README saved status, deferred fields, and next decision |
| 2. Missing destination | `ses_e79528a72ffeyE6AByoqSjrfGf` | Pass: asked for a destination before any workspace read/write; after the natural answer, wrote and reread both files with only the fictional fact |
| 3. Resume checkpoint | `ses_e79522c57ffeb5l7hqmfWF9ZPD` | Pass: native skill call; direct reads of the named workspace README and role; preserved the saved next decision and asked one focused follow-up |

Earlier runs exposed failures that drove the changes: Nano tried unsupported code helpers and claimed nonexistent writes, then tried to create an OpenCode worktree. A no-destination run created an empty workspace after its question tool failed. OpenCode also hid the skill while its manual-only flag was set. During the first resume rerun, Nano tried `execute` for a filesystem probe; when that failed, it listed the test directory before reading the selected workspace. The skill now explicitly forbids code runners and parent-directory searches; the fresh rerun used direct reads of only the named workspace. The current version is discoverable for explicit setup requests, defines a fast path for named folders, verifies writes, and stops when a required answer is unavailable.
