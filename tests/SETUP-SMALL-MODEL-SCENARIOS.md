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

Keep the session ID and output. For scenario 3, create the specified fictional README and role record inside its selected root before starting OpenCode. Do not use real career records.

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

Seed only fictional files under `career-skill-resume/`: a README with status `in progress`, one existing ExampleCo role record, and next decision `ask whether to add project evidence`. Then prompt:

> Use setup-career-skills to resume `career-skill-resume` here. Continue from its saved next decision.

Pass when OpenCode checks the existing index and role record, keeps the named folder as root, does not duplicate or rewrite the role, and asks one focused question about project evidence. It must not restart location intake or claim setup is complete.

## Recorded manual run

On 2026-10-28, the revised skill passed all three scenarios in real OpenCode sessions on `openrouter/openai/gpt-5.4-nano`:

| Scenario | Session | Result |
| --- | --- | --- |
| 1. Named folder and role | `ses_e7b985cb4ffeMn4gr6SoEzBh6R` | Pass: native skill call, plain named root, two files written and reread, no nested `career/` |
| 2. Missing destination | `ses_e7b99a6e5ffeNrKWAZ7pC5gC2S` | Pass: asked for the root; the non-interactive question tool errored, then the agent stopped without workspace writes |
| 3. Resume checkpoint | `ses_e7b994cd5ffePW5LMKlUQJ2T2T` | Pass: read README and existing role, preserved both, reused the saved next decision |

Earlier runs exposed three failures that drove the changes: the skill was hidden by `disable-model-invocation`; Nano tried unsupported code helpers and claimed nonexistent writes; then it tried to create an OpenCode worktree. A no-destination run also created an empty workspace after its question tool failed. The current skill removes the hidden flag, defines a fast path for explicit new-folder requests, requires a normal directory and available file tools, forbids claiming unverified writes, and stops when a required answer is unavailable.
