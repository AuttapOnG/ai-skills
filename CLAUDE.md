# ai-skills

## Project Context
- **Type:** AI-neutral skills registry (markdown/JSON only — no code runtime)
- **Stack:** Markdown + JSON; GitHub Actions CI (Phase 2)
- **Team:** solo maintainer; external contributions via PR

## Context & Memory Rules
At the start of every session:
1. Run `bash init.sh`
2. Read `harness/progress.md` (Current State + Feature index)
3. Load the feature you are working on: its entry in `harness/feature_list.json`
   and its note file `harness/notes/AIS-NNN.md`
4. Load the approved spec: `harness/specs/2026-07-22-ai-skills-registry-design.md`
   — it is the single source of truth for this project.

## Constraints (MEDIUM AUTONOMY)
Proceed autonomously EXCEPT for these actions — always ask first:
- Deleting files or directories
- `git push` or any publish action (this repo is public — a push IS a release)
- Installing new dependencies
- Modifying `.claude/settings.json` or `CLAUDE.md`

For all other actions, proceed and log what you did.

## Project-Specific Rules
- **Public repo hygiene:** nothing under `skills/` may contain personal absolute
  paths (`/Users/...`), company-internal URLs/names, or secrets. init.sh scans;
  CI (Phase 2) enforces.
- **registry.json is generated** from SKILL.md frontmatter — never hand-edit.
- **Skills are markdown-only (v1).** No executable scripts.
- **Skills must be tool-neutral:** discovery ladders instead of hardcoded paths
  or tool-specific names.
- Every commit that changes a skill credits all co-authors (human and AI) via
  `Co-Authored-By` trailers.

## Work Control (harness memory)
`harness/feature_list.json` is the single source of truth for what is done
and what is next. Follow the update discipline in `harness/README.md`:
- Set a feature `in_progress` before starting; `done` only after every
  acceptance criterion is verified.
- Per-feature details go in `harness/notes/AIS-NNN.md`; cross-feature
  decisions go in the dated cross-cutting log in `harness/progress.md`.
- New work discovered mid-feature becomes a new feature entry — never
  silently expand scope.

## Feature Workflow
New work follows: spec in `harness/specs/` (approved by the human) → feature
entries in `harness/feature_list.json` → implementation → verification against
acceptance criteria → commit.

## Self-Verification Checklist
Before saying "done", verify:
- [ ] Task matches the approved spec
- [ ] No unrelated files were modified
- [ ] `bash init.sh` passes (secret/path scans clean, registry in sync)
- [ ] No secrets or personal paths in any diff
- [ ] Commits are clean, descriptive, and carry Co-Authored-By where required
