---
name: self-review
description: Review your own branch changes against project standards, quality, cross-file consistency, and test coverage; present issues as a table, then auto-fix on request.
---

Review and fix all changes in the current branch compared to the main branch.

## Step 1: Detect Base Branch

Determine the base branch by checking (in order):
1. If `develop` branch exists → use `develop`
2. If `main` branch exists → use `main`
3. If `master` branch exists → use `master`
4. Otherwise, ask the user

Store the result as `BASE_BRANCH` for all subsequent commands.

## Step 2: Get Branch Diff

Run these in parallel:
1. `git diff $BASE_BRANCH...HEAD` — full diff of all changes
2. `git diff $BASE_BRANCH...HEAD --name-only` — list of changed files
3. `git log $BASE_BRANCH..HEAD --oneline` — commits on this branch

## Step 3: Analyze Changes

Read each changed file fully to understand context, then review the diff for:

### Project Standards
- Check if a `CLAUDE.md` or similar project guidelines file exists at the repo root
- If found, read it and validate changes against project-specific rules
- Flag violations of any documented coding standards

### Code Quality
- Missing error handling (try/catch, error states)
- Missing or wrong `useCallback` / `useMemo` deps (React projects)
- Accessibility issues (missing aria-*, labels)
- Security issues (XSS, injection, exposed secrets, hardcoded credentials)
- Logic bugs or race conditions
- TypeScript: unjustified `any` types
- Unused imports or dead code introduced in this branch

### Cross-File Analysis
After reviewing individual files, analyze how changed files interact with each other:
- **State / storage lifecycle**: If file A writes state/cookie/storage and file B reads it, verify the full lifecycle — creation, update, AND cleanup.
- **Data flow**: Trace data from source (API response, form input) through transforms to consumers. Flag mismatches in shape, type, or assumptions.
- **Shared utilities**: If a utility was modified, verify ALL callers handle the new signature/behavior correctly.
- **Auth / permission paths**: If auth-related code changed, trace the full chain and flag gaps.

For each cross-file issue found, read the relevant files to confirm the issue before flagging it.

### Unit Test Coverage
- Detect the test framework and test directory layout from project config (e.g., `jest.config.*`, `vitest.config.*`, `pytest.ini`, `go.test`, etc.)
- For each changed source file (excluding test files, types, configs, re-exports):
  - Check if a corresponding test file exists
  - If no test file exists, flag as **Medium**: "Missing unit test file"
  - If significant new logic (hooks, services, utilities, user interaction), upgrade to **High**

Then run **only** tests related to changed files (not the entire suite):
- Auto-detect the test command from project config
- If no related test files exist, skip and note "No related tests to run"
- If any tests **fail**, flag each as **High** with the test name and error

Format all issues as a table:

| Priority | File | Line | Issue | Fix |
|----------|------|------|-------|-----|
| High/Medium/Minor | path/to/file | 42 | Description | How to fix |

## Step 4: Show Review Summary

Output the full review as text:

```
## Self-Review Summary

### Branch
[branch name] → $BASE_BRANCH

### Changed Files
[list of files]

### Commits
[commit list]

### Overview
[what this branch does, 1-2 sentences]

### Unit Test Coverage
[for each changed file: has test / missing test]

### Test Run
[PASSED / FAILED — X tests passed, Y failed — or list failing test names]

### Issues Found
[issues table — or "No issues found" if clean]
```

If **no issues found**, output "No issues found" and stop. Do NOT ask the user.

If **issues were found**, ask the user:

```
question: "Found X issues. Fix them all now?\n\n**Issues:**\n1. [High] file#42 — [issue]\n2. [Medium] file#100 — [issue]"
```

Options:
- "Fix all issues (Recommended)" — proceed to fix
- "Fix High priority only" — fix only High items
- "Show me first, I'll decide per issue" — go through each one
- "Cancel" — do nothing

## Step 5: Fix Issues

Based on user choice, edit the file to fix each issue (never rewrite whole files unless necessary).

For each fix:
1. Read the file first if not already read
2. Make the minimal change to fix the issue
3. For "Missing unit test" issues: create a test file following the project's existing test patterns
4. Report: `Fixed: [file]:[line] — [what was changed]`

After all fixes:
- Run `git diff $BASE_BRANCH...HEAD --stat` to confirm scope of changes
- Output a summary: "Fixed X/Y issues. [list of what was fixed]"

## Important Notes

- Read files before editing — never guess at context
- Make minimal changes — don't refactor code that wasn't asked about
- Don't add comments, docstrings, or type annotations to unchanged code
- Don't create new files unless the fix requires it
- If a fix would break other things, warn the user instead of applying it

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
