# ai-skills — Agent Instructions

## Project
- Type: AI-neutral skills registry (markdown/JSON only — no code runtime)
- Stack: Markdown + JSON; GitHub Actions CI
- Team: solo maintainer; external contributions via PR

## Session Start
1. Run `bash init.sh` if present
2. Read `harness/progress.md` (Current State + Feature index)
3. Load the feature you are working on from `harness/feature_list.json`
   and its note `harness/notes/AIS-NNN.md`
4. Load the approved spec: `docs/specs/2026-07-22-ai-skills-registry-design.md`
   — single source of truth.

## Rules (MEDIUM AUTONOMY)
Ask before:
- Deleting files or directories
- Pushing to git / any publish action (public repo — a push IS a release)
- Installing dependencies

Proceed autonomously for all other actions.

## Project-Specific Rules
- Nothing under `skills/` may contain personal absolute paths, company-internal
  URLs/names, or secrets.
- `registry.json` is generated from SKILL.md frontmatter — never hand-edit.
- Skills are markdown-only (v1) and must be tool-neutral (discovery ladders,
  no hardcoded tool names/paths).
- Commits changing a skill credit all co-authors (human and AI) via
  `Co-Authored-By` trailers.

## Work Control
`harness/feature_list.json` is the single source of truth for work status.
Set a feature `in_progress` before starting; `done` only after every acceptance
criterion is verified. Per-feature notes in `harness/notes/`; cross-feature
decisions in `harness/progress.md`. New work discovered mid-feature becomes a
new feature entry — never silently expand scope.

## Self-Check
- [ ] Matches the approved spec
- [ ] No unrelated changes
- [ ] No secrets or personal paths in diff
- [ ] Co-Authored-By present where required
