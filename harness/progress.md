# Progress

## Current State

**v1 COMPLETE (AIS-001→011); phase-4 follow-ups AIS-012→018.**
AIS-012→016 done & live on main (skill-updater backfill + drift prevention, PR #3).
AIS-017 (MIT LICENSE) + AIS-018 (README sync) done locally — pending push.
Public repo live at https://github.com/AuttapOnG/ai-skills with **9** tool-neutral, markdown-only
skills, generated `registry.json`, README INSTALL/UPDATE protocol, full CONTRIBUTING, CI
(`validate`, green), branch protection on `main`, and `tools/gen_registry.py`. Clean git identity
+ history (personal email; no company tokens anywhere in reachable history).
- Phase 1 (AIS-001→004): repo, skills, README, registry, UC1 install acceptance (live).
- Phase 2 (AIS-005→007): UC2 update acceptance (live), CI, CONTRIBUTING + branch protection.
- Phase 3 (AIS-008→010): skill-publisher, generalized worklog, cross-tool test matrix
  (protocol verified tool-neutral via a real Codex UC1 run).
- AIS-011: xlsx-safe-export → decided SKIP (stays local; markdown-only v1 stands).
- Phase 4 (post-v1, AIS-012→013): skill-updater meta-skill — base UPDATE/UC2 flow (AIS-012)
  + discover-new-skills enhancement (AIS-013). Landed via PR #1/#2, backfilled to harness.
- Phase 4 (AIS-014→016): **skill↔harness drift prevention** — all 3 layers done & live on main
  (PR #3): AIS-014 init.sh parity guard, AIS-016 CONTRIBUTING note, AIS-015 skill-publisher
  work-control step (republished via the merge).

Possible follow-ups (not committed): README polish from the Codex test (AIS-010 note), and the
residual-risk note on force-pushed-away objects (see git-identity entries below).

## Feature index

| ID | Title | Status | Note |
|---|---|---|---|
| AIS-001 | Repo bootstrap (git init, harness, spec, GitHub repo) | done | [notes/AIS-001.md](notes/AIS-001.md) |
| AIS-002 | Migrate & convert skills per spec §7 | done | [notes/AIS-002.md](notes/AIS-002.md) |
| AIS-003 | README protocol (INSTALL/UPDATE) | done | [notes/AIS-003.md](notes/AIS-003.md) |
| AIS-004 | Registry generator + first registry.json + UC1 acceptance | done | [notes/AIS-004.md](notes/AIS-004.md) |
| AIS-005 | Provenance + full UPDATE protocol | done | [notes/AIS-005.md](notes/AIS-005.md) |
| AIS-006 | CONTRIBUTING.md + branch protection | done | [notes/AIS-006.md](notes/AIS-006.md) |
| AIS-007 | CI validate.yml | done | [notes/AIS-007.md](notes/AIS-007.md) |
| AIS-008 | skill-publisher meta-skill | done | [notes/AIS-008.md](notes/AIS-008.md) |
| AIS-009 | Generalize worklog and publish | done | [notes/AIS-009.md](notes/AIS-009.md) |
| AIS-010 | Test matrix UC1–UC4 on Claude Code + Codex | done | [notes/AIS-010.md](notes/AIS-010.md) |
| AIS-011 | Decide xlsx-safe-export disposition (deferred from AIS-002) | done | [notes/AIS-011.md](notes/AIS-011.md) |
| AIS-012 | skill-updater meta-skill (base UPDATE/UC2 flow) | done | [notes/AIS-012.md](notes/AIS-012.md) |
| AIS-013 | skill-updater: discover skills new in the registry | done | [notes/AIS-013.md](notes/AIS-013.md) |
| AIS-014 | Drift prevention L2: init.sh skill↔harness parity guard | done | [notes/AIS-014.md](notes/AIS-014.md) |
| AIS-015 | Drift prevention L1: skill-publisher updates work-control memory | done | [notes/AIS-015.md](notes/AIS-015.md) |
| AIS-016 | Drift prevention L3: CONTRIBUTING maintainer work-tracking note | done | [notes/AIS-016.md](notes/AIS-016.md) |
| AIS-017 | LICENSE (MIT, © 2026 Auttapong Tura) | done | [notes/AIS-017.md](notes/AIS-017.md) |
| AIS-018 | README sync (License section, UPDATE new-skills step, meta-skills note) | done | [notes/AIS-018.md](notes/AIS-018.md) |

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
- 2026-07-22 — **Public-hygiene scrub completed** (extends the identity fix). Found that the
  email rewrite alone was insufficient: earlier intermediate commits still had the company
  name + internal issue tracker URL in their *content* (plan/notes), and they'd been pushed. Ran a
  full-history CONTENT rewrite (filter-branch tree-filter) replacing all company tokens with
  `<company>` placeholders across every commit, then force-pushed. Verified against the remote:
  zero company tokens in any commit reachable from origin/main; all author emails personal.
  **Lesson: genericize BEFORE the first commit, and GATE every push on the leak scan (abort, not
  echo).** Residual risk to note: force-pushed-away commits may linger as unreachable objects in
  GitHub until GC / via direct SHA; for guaranteed purge on a sensitive leak, contact GitHub Support.
- 2026-07-22 — Phase 3 done: AIS-008 (skill-publisher) ✓, AIS-009 (worklog generalized +
  published, subagent-driven via Codex) ✓, AIS-010 (cross-tool test matrix; Codex followed the
  README INSTALL protocol end-to-end → protocol confirmed tool-neutral) ✓.
- 2026-07-22 — **PROJECT COMPLETE.** AIS-006 branch protection set on `main` (Standard: PR + 1
  review + `validate` check for non-owners; owner/admin bypass). AIS-011 decided: **skip**
  xlsx-safe-export (stays local; markdown-only v1 unchanged). All 11 features done.
- 2026-07-22 — Extended hygiene (user request): removed ALL remaining third-party product-name
  references (issue-tracker / wiki / team-chat tooling) from the maintainer docs across the FULL
  history — genericized to neutral terms — so there is zero reference to the maintainer's original
  corporate toolchain. Full-history tree-filter scrub + force-push; verified zero such references
  in any reachable commit.
- 2026-07-22 — **Process gap caught (user): skill-updater merged without a harness entry.**
  The skill landed via two PRs — #1 `d32eb39` (base UPDATE/UC2 flow) and #2 `9ff443e`
  (discover-new-skills) — but both touched only `registry.json` + `skills/skill-updater/SKILL.md`,
  **never `harness/`**. So the skill + registry were correct and in sync, yet feature_list.json
  still stopped at AIS-011 and progress.md still read "PROJECT COMPLETE — 11 features". This
  violated CLAUDE.md's rule that new work becomes a feature entry. **Backfilled** (user chose the
  2-feature split): AIS-012 (base flow) + AIS-013 (discovery enhancement), both `done`, phase 4
  (post-v1); notes AIS-012.md / AIS-013.md written; index + skill count (8→9) updated.
  **Lesson: a PR that adds/changes a skill must also add/update its feature entry — gate this in
  review (and consider a CI check that every `skills/<name>` has a matching feature_list entry).**
- 2026-07-22 — **Drift-prevention built (AIS-014→016)** after the user asked how to stop this
  recurring. Reframe: the harness is maintainer-private, NOT part of the registry's public
  contract — so two publish paths need two fixes, plus a backstop. **L2 (AIS-014, done):** init.sh
  now word-boundary-greps every `skills/<name>` across all of `harness/` and WARNs if unreferenced
  — the backstop that catches drift from any path at session start (negative-tested). **L1
  (AIS-015, in_progress):** skill-publisher gained a conditional "update the project's work-control
  memory" step (tool-neutral; skips if no harness) — closes the self-publish path, but it edits a
  *published* skill so it needs a republish/push (user-gated) to land. **L3 (AIS-016, done):**
  CONTRIBUTING now states maintainers record merged skills in `harness/` + a review-checklist item.
  Chose **init.sh over public CI** for enforcement: a CI parity check would fail external PRs that
  correctly don't touch the private harness.
- 2026-07-22 — **AIS-012→016 landed on main via PR #3** (rebase-merge, keeping the two atomic
  commits `dcd2643` backfill + `4b349d0` drift-prevention; CI `validate` green). Branch protection
  required 1 review — merged with the **owner/admin bypass** (solo maintainer can't self-approve),
  same as #1/#2. skill-publisher is now republished on public main → **AIS-015 done**; all phase-4
  follow-ups complete. Note: pushes are gated by the settings.json push-hook + the auto-mode
  classifier — the branch push and the PR merge were both performed by the human.
- 2026-07-22 — **Repo housekeeping (user prompt): licensing + README currency.** (1) AIS-017:
  added a root MIT `LICENSE` (© 2026 Auttapong Tura). The registry had **no license** — a public
  install/contribute repo defaults to all-rights-reserved, which forbade the very reuse the
  INSTALL protocol asks for. MIT chosen over CC BY 4.0 / Apache-2.0 for lowest friction (footer
  already carries attribution). (2) AIS-018: README synced — License section, a new "surface
  skills new in the registry" step in the UPDATE protocol (it had drifted behind skill-updater/
  AIS-013), and a note that INSTALL/UPDATE/publish are also installable as skill-updater /
  skill-publisher. README still points to registry.json as the index (no per-skill listing), so
  the new skill itself needed no README change. Both done locally; awaiting the human push.
