# Harness — ai-skills

Work-control memory for developing the ai-skills registry.

- `specs/` — approved designs. Start with `2026-07-22-ai-skills-registry-design.md` — it is the single source of truth for this project.
- `feature_list.json` — AIS-XXX features across 3 phases. Update `status` as work proceeds (pending → in_progress → done).
- `progress.md` — append a dated entry per working session.
- `notes/` — one note per feature (AIS-001.md, ...) capturing decisions, test results, and gotchas.

Rules:
- Read the spec before implementing anything.
- A phase is done only when its acceptance criteria in spec §8 pass, verified live (not assumed).
- Phase 3 requires the test matrix on BOTH Claude Code and Codex.
