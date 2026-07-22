# Progress

## Current State

Design approved and spec written (v1). Harness scaffold complete (CLAUDE.md,
AGENTS.md, init.sh, settings hooks, ADR-0001). **AIS-001 done:** repo is live,
public, and pushed at https://github.com/AuttapOnG/ai-skills (name confirmed
`ai-skills`; origin/main == HEAD == f1ccc3d).
**AIS-002 done:** 6 skills migrated (self-review, commit, enhance, pr, cli-subagents,
init-harness) — tool-neutral, markdown-only, frontmatter + footer, committed locally with
Co-Authored-By (Claude + Codex). Executed subagent-driven with Codex CLI as executor.
**AIS-003 done:** README (INSTALL/UPDATE protocol for AI agents) + CONTRIBUTING stub committed.
Next: **AIS-004** (registry generator + first registry.json + real UC1 install). registry.json
not generated yet. Nothing pushed since f1ccc3d — first push is gated for the AIS-004 UC1
acceptance checkpoint. Plan: `docs/plans/2026-07-22-phase1-skill-migration.md`.

## Feature index

| ID | Title | Status | Note |
|---|---|---|---|
| AIS-001 | Repo bootstrap (git init, harness, spec, GitHub repo) | done | [notes/AIS-001.md](notes/AIS-001.md) |
| AIS-002 | Migrate & convert skills per spec §7 | done | [notes/AIS-002.md](notes/AIS-002.md) |
| AIS-003 | README protocol (INSTALL/UPDATE) | done | [notes/AIS-003.md](notes/AIS-003.md) |
| AIS-004 | Registry generator + first registry.json + UC1 acceptance | pending | [notes/AIS-004.md](notes/AIS-004.md) |
| AIS-005 | Provenance + full UPDATE protocol | pending | [notes/AIS-005.md](notes/AIS-005.md) |
| AIS-006 | CONTRIBUTING.md + branch protection | pending | [notes/AIS-006.md](notes/AIS-006.md) |
| AIS-007 | CI validate.yml | pending | [notes/AIS-007.md](notes/AIS-007.md) |
| AIS-008 | skill-publisher meta-skill | pending | [notes/AIS-008.md](notes/AIS-008.md) |
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
