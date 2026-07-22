# Progress

## Current State

Public repo live at https://github.com/AuttapOnG/ai-skills. **Phase 1 + most of Phase 2 done.**
- Phase 1 (AIS-001→004): 6 tool-neutral skills, README INSTALL/UPDATE protocol, generated
  `registry.json`, `tools/gen_registry.py`, wired `init.sh`. UC1 install acceptance passed live.
- Phase 2: AIS-005 (UPDATE/UC2 acceptance passed live) ✓, AIS-007 (CI validate.yml, green run) ✓,
  AIS-006 CONTRIBUTING ✓ (branch protection deferred to end, to avoid blocking owner pushes).

Driving to full completion with standing push approval (leak scan before each push; stop only for
branch protection + AIS-011). **Next: Phase 3** — AIS-008 (skill-publisher meta-skill), AIS-009
(generalize + publish worklog), AIS-010 (UC1–UC4 test matrix on Claude Code + Codex) → branch
protection → **AIS-011** (xlsx-safe-export decision). Plan:
`docs/plans/2026-07-22-phase1-skill-migration.md`.

## Feature index

| ID | Title | Status | Note |
|---|---|---|---|
| AIS-001 | Repo bootstrap (git init, harness, spec, GitHub repo) | done | [notes/AIS-001.md](notes/AIS-001.md) |
| AIS-002 | Migrate & convert skills per spec §7 | done | [notes/AIS-002.md](notes/AIS-002.md) |
| AIS-003 | README protocol (INSTALL/UPDATE) | done | [notes/AIS-003.md](notes/AIS-003.md) |
| AIS-004 | Registry generator + first registry.json + UC1 acceptance | done | [notes/AIS-004.md](notes/AIS-004.md) |
| AIS-005 | Provenance + full UPDATE protocol | done | [notes/AIS-005.md](notes/AIS-005.md) |
| AIS-006 | CONTRIBUTING.md + branch protection | in_progress | [notes/AIS-006.md](notes/AIS-006.md) |
| AIS-007 | CI validate.yml | done | [notes/AIS-007.md](notes/AIS-007.md) |
| AIS-008 | skill-publisher meta-skill | done | [notes/AIS-008.md](notes/AIS-008.md) |
| AIS-009 | Generalize worklog and publish | pending | [notes/AIS-009.md](notes/AIS-009.md) |
| AIS-010 | Test matrix UC1–UC4 on Claude Code + Codex | pending | [notes/AIS-010.md](notes/AIS-010.md) |
| AIS-011 | Decide xlsx-safe-export disposition (deferred from AIS-002) | pending | — |

## Cross-cutting decisions & events

- 2026-07-22 — Design finalized via brainstorming: no symlinks (copy + provenance), registry generated from frontmatter, markdown-only v1, ask-before-share/publish, Co-Authored-By required. See spec §9 decision log.
- 2026-07-22 — Harness initialized (ADR-0001): medium autonomy, checkpoints = git push + file deletion, MODERATE permissions (network open — UC protocols need GitHub API).
- 2026-07-22 — Open question RESOLVED: repo name = `ai-skills`; repo created public at
  https://github.com/AuttapOnG/ai-skills (owner `AuttapOnG`) and pushed. AIS-001 done.
- 2026-07-22 — AIS-002 audit surfaced a spec conflict: §7 lists `xlsx-safe-export` for
  Phase 1 migration, but its core is a Python validator, which §6.2/§9 forbid (markdown-only).
  Resolution proposed in the Phase 1 plan: DEFER xlsx-safe-export to a new feature (AIS-011)
  pending a policy decision — do not silently expand AIS-002 scope. Also found: `pr.md`
  leaks `<issue-tracker-host>` (public-hygiene blocker); `commit.md` contains a
  "Do not add Co-Authored-By" line that contradicts the registry's co-author rule.
- 2026-07-22 — AIS-002 done: 6 skills migrated & committed (subagent-driven, Codex CLI as
  executor; ~84k tokens on Codex's quota). All leak/gate checks clean; `pr` company URL and
  `commit` co-author contradiction fixed. xlsx-safe-export deferred → AIS-011 opened.
  Nothing pushed (still f1ccc3d on origin) — first push is the AIS-004 UC1 checkpoint.
- 2026-07-22 — **Structure realigned to the init-harness skill's standard layout** (user
  decision): design docs moved `harness/{specs,adr,plans}` → top-level `docs/{specs,adr,plans}`
  via `git mv`; `harness/` now holds only work-control (feature_list, progress, notes, evals,
  traces). This **reverses ADR-0001 decision #2** (which had deliberately kept specs/ADRs under
  `harness/`); ADR-0001 updated in place to reflect the new layout. All references updated
  (CLAUDE.md, AGENTS.md, spec §2, init.sh, feature_list, notes, plan). Empty `harness/{specs,adr,plans}`
  dirs left on disk (git untracks empty dirs) — remove manually if desired (rmdir is hook-gated).
- 2026-07-22 — Pre-push hygiene: company strings (`<company>`/`<issue-tracker-host>`)
  genericized in maintainer docs; scan patterns moved to git-ignored `.scan-local-patterns`
  (init.sh reads it). Confirmed zero company strings in any tracked file before the push.
- 2026-07-22 — **PHASE 1 COMPLETE**: first public release pushed (origin/main `5fd9670`,
  12 commits). UC1 install acceptance passed end-to-end from the live GitHub repo (spec §8).
  The push succeeded (settings.json push-hook did not intercept in this run) — user had
  pre-approved it.
- 2026-07-22 — User granted STANDING push approval to finish the whole project; I run the
  full leak scan before each push and stop only for branch protection + the AIS-011 decision.
- 2026-07-22 — **Phase 2 mostly done**: AIS-005 (UPDATE/UC2) + AIS-007 (CI validate.yml) done
  and verified live (CI run green `76694c7`; UC2 detected `pr` update + showed commit log +
  applied + local_modified guard). AIS-006 CONTRIBUTING done; **branch protection deferred to
  end** (avoid blocking remaining owner pushes). Next: Phase 3 (AIS-008/009/010) → branch
  protection → AIS-011 decision.
- 2026-07-22 — **Git identity fixed** (user caught it): commits were authored with a work
  (company) email from the global ~/.gitconfig on this PUBLIC PERSONAL repo. Set repo-LOCAL
  identity to the personal address `ace.auttapong@gmail.com`; rewrote all 22 commits
  (author+committer, filter-branch, names/dates/messages/Co-Authored-By preserved) and
  force-pushed. origin now 100% personal email; the work email was removed from public history.
  (For attribution, ensure the personal email is added to the AuttapOnG GitHub account.)
- 2026-07-22 — AIS-008 done: skill-publisher meta-skill (UC4 flow) published; registry now 7
  skills; CI green. CI caught a `/Users/` literal in its audit text (run failure) → fixed →
  green — doubles as a live negative test that CI rejects violations.
