# AGENTS.md Template

Cross-runtime portable version of CLAUDE.md. Do NOT include Claude Code-specific syntax
(no hook references, no settings.json references, no .claude/ paths).

Replace all [PLACEHOLDERS] with user answers. Use the section matching autonomy level.

---

## LOW AUTONOMY variant

```markdown
# [PROJECT_NAME] — Agent Instructions

## Project
- Type: [PROJECT_TYPE]
- Stack: [STACK]
- Team: [TEAM_SIZE]

## Session Start
At the start of every session:
1. Run `bash init.sh` if present
2. Read any spec in `docs/specs/` marked approved
3. Check for uncommitted changes — stop and ask if unexpected ones exist

## Rules (LOW AUTONOMY)
- Ask before creating, modifying, or deleting any file
- Ask before running shell commands
- Ask before making network requests
- Check in after every 2 actions maximum

## Workflow
- Read spec before starting any task
- Confirm understanding before writing code
- Run self-check before claiming done

## Self-Check
- [ ] Matches spec
- [ ] No unrelated changes
- [ ] No secrets in diff
```

---

## MEDIUM AUTONOMY variant

```markdown
# [PROJECT_NAME] — Agent Instructions

## Project
- Type: [PROJECT_TYPE]
- Stack: [STACK]
- Team: [TEAM_SIZE]

## Session Start
1. Run `bash init.sh` if present
2. Read approved specs in `docs/specs/`

## Rules (MEDIUM AUTONOMY)
Ask before:
- Deleting files
- Pushing to git / deploying
- External network calls
- Installing dependencies

Proceed autonomously for all other actions.

## Self-Check
- [ ] Matches spec
- [ ] No unrelated changes
- [ ] No secrets in diff
```

---

## HIGH AUTONOMY variant

```markdown
# [PROJECT_NAME] — Agent Instructions

## Project
- Type: [PROJECT_TYPE]
- Stack: [STACK]
- Team: [TEAM_SIZE]

## Session Start
1. Run `bash init.sh` if present
2. Load approved specs

## Rules (HIGH AUTONOMY)
Act autonomously. Log significant actions in WORKING_STATE.md.
Prefer small reversible changes. Commit frequently.

## Self-Check
- [ ] Matches spec
- [ ] Tests pass
- [ ] No secrets in diff
- [ ] WORKING_STATE.md updated
```
