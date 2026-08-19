# CLAUDE.md Template

Use the section matching the chosen autonomy level. Replace all [PLACEHOLDERS] with user answers.

---

## LOW AUTONOMY variant

```markdown
# [PROJECT_NAME]

## Project Context
- **Type:** [PROJECT_TYPE]
- **Stack:** [STACK]
- **Team:** [TEAM_SIZE]

## Context & Memory Rules
At the start of every session:
1. Run `bash init.sh`
2. Read `harness/progress.md` (Current State + Feature index)
3. Load the feature you are working on: its entry in
   `harness/feature_list.json` and its note `harness/notes/[PREFIX]-NNN.md`
4. Read `docs/specs/` — load any spec marked `status: approved`
5. Read `docs/adr/` — understand past decisions
6. Check `git status` — do not proceed if there are unexpected uncommitted changes

During long tasks, record state in the current feature's note after each meaningful step.

## Constraints (LOW AUTONOMY)
Pre-approved (no need to ask): `bash init.sh` at session start, read-only
commands (`git status`, `git log`, `git diff`, listing and reading files),
and updates to the harness memory (`harness/progress.md`, `harness/notes/`).
You MUST ask for explicit approval before anything else, including:
- Creating, modifying, or deleting any other file
- Running any other shell command
- Making any network request
- Installing any dependency
- Committing or pushing to git

Do not chain more than 2 actions without a checkpoint.

## Workflow
1. Read the spec in `docs/specs/` before starting any task
2. Confirm your understanding with the user before writing code
3. After each file change, pause and summarize what changed
4. Run the self-verification checklist before claiming completion

## Self-Verification Checklist
Before saying "done", verify:
- [ ] The task matches the approved spec
- [ ] No unrelated files were modified
- [ ] Tests pass (if applicable)
- [ ] No secrets or credentials appear in any diff
- [ ] `git diff` is clean and scoped to the task
```

---

## MEDIUM AUTONOMY variant

```markdown
# [PROJECT_NAME]

## Project Context
- **Type:** [PROJECT_TYPE]
- **Stack:** [STACK]
- **Team:** [TEAM_SIZE]

## Context & Memory Rules
At the start of every session:
1. Run `bash init.sh`
2. Read `harness/progress.md` (Current State + Feature index)
3. Load the current feature's entry in `harness/feature_list.json` and its
   note `harness/notes/[PREFIX]-NNN.md`
4. Read any spec in `docs/specs/` marked `status: approved`
5. Check `git status`

## Constraints (MEDIUM AUTONOMY)
Proceed autonomously EXCEPT for these actions — always ask first:
- Deleting files or directories
- `git push` or any deploy command
- External API calls or network requests
- Installing new dependencies
- Modifying `.claude/settings.json` or `CLAUDE.md`

For all other actions, proceed and log what you did.

## Workflow
1. Read the spec before starting
2. Work in small commits — one logical change per commit
3. Run the self-verification checklist before claiming completion

## Self-Verification Checklist
Before saying "done", verify:
- [ ] Task matches the approved spec
- [ ] No unrelated files were modified
- [ ] Tests pass (if applicable)
- [ ] No secrets in any diff
- [ ] Commits are clean and descriptive
```

---

## HIGH AUTONOMY variant

```markdown
# [PROJECT_NAME]

## Project Context
- **Type:** [PROJECT_TYPE]
- **Stack:** [STACK]
- **Team:** [TEAM_SIZE]

## Context & Memory Rules
At the start of every session:
1. Run `bash init.sh`
2. Read `harness/progress.md` (Current State + Feature index)
3. Load the current feature's entry in `harness/feature_list.json` and its
   note `harness/notes/[PREFIX]-NNN.md`
4. Load any approved spec from `docs/specs/`

## Constraints (HIGH AUTONOMY)
You may act autonomously on all tasks. Maintain an audit trail:
- Log every significant action in the current feature's note (`harness/notes/[PREFIX]-NNN.md`)
- Commit frequently with descriptive messages
- Never modify `.claude/settings.json` or `CLAUDE.md` without recording it in the cross-cutting log in `harness/progress.md`

## Workflow
1. Read spec → plan → execute → verify → commit
2. Prefer small, reversible changes over large sweeping edits
3. Run self-verification before closing any task

## Self-Verification Checklist
Before saying "done", verify:
- [ ] Task matches spec
- [ ] All tests pass
- [ ] No secrets in diff
- [ ] Harness memory updated (feature note + progress.md)
```
