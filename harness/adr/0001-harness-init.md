# ADR-0001: Harness Initialization

**Date:** 2026-07-22
**Status:** accepted

## Context
This project needed a harness engineering scaffold to make agent work reliable and observable.
The harness was initialized using `/init-harness` based on the following project profile:

- Project type: AI-neutral skills registry (markdown/JSON only, no code runtime)
- Stack: Markdown + JSON; GitHub Actions CI (Phase 2)
- Team size: solo maintainer, external contributors via PR
- Autonomy level: medium
- Checkpoints: before git push, before file deletion
- Environment: public-facing (the repo is the published product)
- Sensitive data: none (enforced — public repo)
- Deploy target: none (GitHub itself is distribution)

## Decision
Initialize a harness scaffold with medium autonomy constraints, push + deletion
checkpoint hooks, and MODERATE permissions.

Deviations from the default init-harness mapping, chosen deliberately:
1. **MODERATE permissions instead of STRICT** (mapping suggests STRICT for
   public/production): the registry's own protocols (UC1/UC2) require GitHub
   API access, and the user chose not to gate network calls. Public-repo
   hygiene is enforced by init.sh scans + CI (AIS-007) instead of blanket
   network denial.
2. **Specs live in `harness/specs/`, ADRs in `harness/adr/`** (not `docs/`):
   preserves this project's pre-existing convention (spec §2) and keeps all
   maintainer material under one visible `harness/` directory.
3. **No example-spec.md**: a real approved spec already exists
   (`harness/specs/2026-07-22-ai-skills-registry-design.md`) and serves as
   the example.
4. **Existing feature IDs AIS-001…010 preserved**; harness initialization is
   recorded as part of AIS-001 (repo bootstrap), now `in_progress`.

## Consequences
- Agents operating in this repo follow CLAUDE.md and AGENTS.md constraints.
- init.sh must be run at the start of each session; it scans for secrets,
  personal/internal paths, and registry desync.
- git push and file deletion are gated by settings.json hooks.
- Harness can be evolved by editing these files; changes recorded as new ADRs.
