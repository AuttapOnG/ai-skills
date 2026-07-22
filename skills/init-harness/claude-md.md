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
2. Read `docs/specs/` — load any spec marked `status: approved`
3. Read `docs/adr/` — understand past decisions
4. Check `git status` — do not proceed if there are unexpected uncommitted changes

Keep a running `WORKING_STATE.md` in project root during long tasks. Update it after each meaningful step.

## Constraints (LOW AUTONOMY)
You MUST ask for explicit approval before:
- Creating, modifying, or deleting ANY file
- Running any shell command
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
2. Read any spec in `docs/specs/` marked `status: approved`
3. Check `git status`

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
2. Load any approved spec from `docs/specs/`

## Constraints (HIGH AUTONOMY)
You may act autonomously on all tasks. Maintain an audit trail:
- Log every significant action to `WORKING_STATE.md`
- Commit frequently with descriptive messages
- Never modify `.claude/settings.json` or `CLAUDE.md` without noting it in `WORKING_STATE.md`

## Workflow
1. Read spec → plan → execute → verify → commit
2. Prefer small, reversible changes over large sweeping edits
3. Run self-verification before closing any task

## Self-Verification Checklist
Before saying "done", verify:
- [ ] Task matches spec
- [ ] All tests pass
- [ ] No secrets in diff
- [ ] WORKING_STATE.md updated
```
