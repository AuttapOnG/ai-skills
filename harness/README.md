# Harness — ai-skills

Work-control memory for developing the ai-skills registry.

## Files

- `specs/` — approved designs. Start with `2026-07-22-ai-skills-registry-design.md` — the single source of truth for this project. New specs from `SPEC-TEMPLATE.md`.
- `adr/` — architecture decision records (start at `0001-harness-init.md`).
- `feature_list.json` — the implementation queue. Every unit of work is a feature with an ID (AIS-NNN), phase, and status (`pending` / `in_progress` / `done`). Single source of truth for what is done and what is next.
- `progress.md` — slim, bounded memory with exactly three sections: **Current State**, **Feature index**, **Cross-cutting decisions & events**.
- `notes/AIS-NNN.md` — one note file per feature: decisions, gotchas, test results.
- `evals/` — agent behavior evaluations (Phase 3 test matrix lives here). `traces/` — observability stub.

## Update discipline

1. Set a feature `in_progress` in `feature_list.json` before starting it.
2. Record decisions and surprises in `notes/AIS-NNN.md` as you go.
3. On completion: verify every acceptance criterion (spec §8), set status `done`, update **Current State** and the **Feature index** in `progress.md`.
4. Decisions affecting more than one feature go in **Cross-cutting decisions & events** (dated, one bullet each).
5. New work discovered mid-feature becomes a NEW feature entry — never silently expand scope.
6. A phase is done only when its acceptance criteria pass, verified live (not assumed). Phase 3 requires the test matrix on BOTH Claude Code and Codex.

Environment bootstrap: `bash init.sh` (from repo root).
