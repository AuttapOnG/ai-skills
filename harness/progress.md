# Progress

## Current State

Design approved and spec written (v1). Harness scaffold complete (CLAUDE.md,
AGENTS.md, init.sh, settings hooks, ADR-0001). Local git repo initialized.
Next: confirm repo name → create GitHub repo → AIS-002 skill migration.
Nothing under `skills/` exists yet; registry not generated yet.

## Feature index

| ID | Title | Status | Note |
|---|---|---|---|
| AIS-001 | Repo bootstrap (git init, harness, spec, GitHub repo) | in_progress | [notes/AIS-001.md](notes/AIS-001.md) |
| AIS-002 | Migrate & convert skills per spec §7 | pending | [notes/AIS-002.md](notes/AIS-002.md) |
| AIS-003 | README protocol (INSTALL/UPDATE) | pending | [notes/AIS-003.md](notes/AIS-003.md) |
| AIS-004 | Registry generator + first registry.json + UC1 acceptance | pending | [notes/AIS-004.md](notes/AIS-004.md) |
| AIS-005 | Provenance + full UPDATE protocol | pending | [notes/AIS-005.md](notes/AIS-005.md) |
| AIS-006 | CONTRIBUTING.md + branch protection | pending | [notes/AIS-006.md](notes/AIS-006.md) |
| AIS-007 | CI validate.yml | pending | [notes/AIS-007.md](notes/AIS-007.md) |
| AIS-008 | skill-publisher meta-skill | pending | [notes/AIS-008.md](notes/AIS-008.md) |
| AIS-009 | Generalize worklog and publish | pending | [notes/AIS-009.md](notes/AIS-009.md) |
| AIS-010 | Test matrix UC1–UC4 on Claude Code + Codex | pending | [notes/AIS-010.md](notes/AIS-010.md) |

## Cross-cutting decisions & events

- 2026-07-22 — Design finalized via brainstorming: no symlinks (copy + provenance), registry generated from frontmatter, markdown-only v1, ask-before-share/publish, Co-Authored-By required. See spec §9 decision log.
- 2026-07-22 — Harness initialized (ADR-0001): medium autonomy, checkpoints = git push + file deletion, MODERATE permissions (network open — UC protocols need GitHub API).
- 2026-07-22 — Open question: repo name (proposal `ai-skills`) — confirm before creating GitHub repo.
