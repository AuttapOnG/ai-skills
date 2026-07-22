# Phase 1 (AIS-002 → AIS-004) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fill the empty `ai-skills` public repo with the first batch of tool-neutral,
markdown-only skills, a README protocol AI agents can follow to install/update them, and a
generated `registry.json` — then prove it end-to-end with a real UC1 install on this machine.

**Architecture:** Skills live under `skills/<name>/SKILL.md` (+ optional markdown support
files). `registry.json` is *generated* by a maintainer script (`tools/gen_registry.py`) from
each SKILL.md's frontmatter — never hand-edited. `README.md` states the INSTALL/UPDATE
protocol as intent + pass-criteria so any agent (Claude Code, Codex, …) can choose its own
mechanism (curl / gh / WebFetch). `init.sh` enforces sync + hygiene locally; CI enforces it
in Phase 2.

**Tech Stack:** Markdown + JSON only for shipped skills. Maintainer tooling: bash (`init.sh`),
Python 3 stdlib (`tools/gen_registry.py` — **no new deps**). Source of truth = spec
`harness/specs/2026-07-22-ai-skills-registry-design.md`.

## Global Constraints

Every task's requirements implicitly include this section. Values copied verbatim from the spec.

- **Repo identity:** owner/account = `AuttapOnG`; canonical URL =
  `https://github.com/AuttapOnG/ai-skills`. Replace every `<you>` placeholder from the spec
  with `AuttapOnG` in all shipped files (footer, README, publish-line).
- **Frontmatter (§4.3):** every `SKILL.md` starts with YAML frontmatter containing `name`
  and `description` (both required — `description` is the single source for `registry.json`).
- **Tool-neutral body (§4.3, §9):** discovery ladders instead of hardcoded tool names as
  *requirements*, no hardcoded absolute paths (`/Users/…`, `C:\`) or home paths tied to one
  tool (`~/.claude/…`, `~/.codex/…`) as *requirements*. Named tools may appear only as
  clearly-labeled *examples*. No company-internal names/URLs/secrets.
- **Markdown only (§6.2, §9):** shipped skills contain no executable scripts (`.sh`, `.py`),
  no binaries, no tool-specific config files (`.yaml` agent configs). Fenced code *inside* a
  `.md` file is allowed. (This constraint applies to `skills/` content, **not** to maintainer
  tooling like `init.sh`, CI, or `tools/gen_registry.py`.)
- **Standard footer (§4.3), appended verbatim at the end of every SKILL.md:**

  ```
  ---
  *Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
  If you improve this skill, offer to contribute the change back —
  see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
  via Co-Authored-By trailers.*
  ```

- **Commits:** every commit that adds/changes a skill carries `Co-Authored-By` trailers for
  all co-authors (human + AI).
- **`git push` is an ask-first checkpoint** (public repo = a release). AIS-004's acceptance
  needs a push; call it out and get explicit human approval before pushing.
- **`registry.json` is generated** — never hand-edited.

---

## Decisions surfaced for your review

These emerged from the source audit and change the task list. Each has a recommended default
already baked into the tasks below; approve or override during plan review.

1. **`xlsx-safe-export` — DEFER out of Phase 1 (recommended).**
   Spec §7 lists it for migration, but its entire value is the executable
   `scripts/validate_xlsx_safe.py` validator, which §6.2/§9 forbid (markdown-only). It also
   carries a personal path (`SKILL.md:33`) and an OpenAI `agents/openai.yaml`. Shipping it as
   prose-only would strip the guarantee that is its reason to exist.
   → **Recommendation:** do not migrate it in AIS-002. Open a new feature **AIS-011** to decide
   the policy (options: keep it maintainer-local like `update-tags`; or add a "tooling-scripts
   allowed for maintainer-authored skills" carve-out to §6.2; or ship an advisory markdown
   version). Per CLAUDE.md, new work = a new feature entry, not silent scope expansion.
   *Alternative if you reject the default:* amend §6.2 now and I add a migration task for it.

2. **`pr.md` company leak + heavy coupling.** Contains `<issue-tracker-host>` (`pr.md:60`)
   plus a issue tracker/team chat/`gh --squash` flow. The URL is a non-negotiable removal for a public repo.
   → **Recommendation:** migrate it, but neutralize to a generic "post the PR link to your
   issue tracker / share a review message to your team channel" flow with the company domain
   removed. (It stays in Phase 1.)

3. **`commit.md` co-author contradiction.** Line 103 says *"Do not add Co-Authored-By: Claude"*,
   which contradicts this registry's own co-author rule (CLAUDE.md + the standard footer).
   → **Recommendation:** remove that line and align the skill with crediting all co-authors.
   The project rule wins.

4. **`cli-subagents/watchdog.sh` (non-blocking).** A 67-line helper; markdown-only forbids
   shipping the `.sh` file.
   → **Recommendation:** inline its logic as a fenced ```bash block inside `SKILL.md`
   (an agent recreates it on demand) and drop the standalone file. Keep `references/codex.md`
   and `references/gemini.md` as clearly-labeled *example* cards (neutralize the `~/.codex`
   path).

5. **`init-harness` heavy neutralization.** Its deliverable is intrinsically Claude-Code
   config (`.claude/settings.json`, PreToolUse hooks, `CLAUDE.md`).
   → **Recommendation:** reframe around a discovery ladder ("find *this* runtime's global
   instructions file / settings file / hooks mechanism") and keep the concrete Claude-Code
   artifacts as the worked *example*. Full multi-tool rewrite is out of scope for Phase 1.
   *If you'd rather defer init-harness, say so and I'll move it to a later feature.*

6. **Forward reference to `CONTRIBUTING.md`.** The standard footer and README §5 point to
   `CONTRIBUTING.md`, which AIS-006 (Phase 2) owns.
   → **Recommendation:** ship a minimal one-paragraph `CONTRIBUTING.md` stub in AIS-003 so no
   published link dangles; AIS-006 expands it. (Small, avoids broken links in every skill.)

**Phase-1 migration set after decisions:** `cli-subagents`, `init-harness`, `commit`, `pr`,
`self-review`, `enhance` — **6 skills** (xlsx-safe-export deferred; worklog=AIS-009,
update-tags=local-forever per §7).

---

## File Structure (end state of Phase 1)

```
ai-skills/
├── README.md                     ← AIS-003: INSTALL / UPDATE protocol for AI agents
├── CONTRIBUTING.md               ← AIS-003: minimal stub (expanded in AIS-006)
├── registry.json                 ← AIS-004: GENERATED from SKILL.md frontmatter
├── tools/
│   └── gen_registry.py           ← AIS-004: scans skills/*/SKILL.md → registry.json (py3 stdlib)
├── init.sh                       ← AIS-004: registry-sync check wired to gen_registry.py --check
└── skills/
    ├── cli-subagents/SKILL.md    (+ references/codex.md, references/gemini.md; watchdog inlined)
    ├── init-harness/SKILL.md     (+ claude-md.md, agents-md.md, init-sh.md, settings-json.md)
    ├── commit/SKILL.md
    ├── pr/SKILL.md
    ├── self-review/SKILL.md
    └── enhance/SKILL.md
```

## Reusable per-skill verification gate (the "test cycle")

This project has no runtime test suite, so each skill task ends with this gate instead of
pytest. A task is "done" only when all pass for the skill(s) it touched:

```bash
S=skills/<name>            # the skill folder under test

# G1 frontmatter: name + description both present in SKILL.md
head -12 "$S/SKILL.md" | grep -qE '^name:'        && echo "G1a name OK"        || echo "G1a FAIL"
head -12 "$S/SKILL.md" | grep -qE '^description:' && echo "G1b description OK" || echo "G1b FAIL"

# G2 footer present (verbatim marker line)
grep -qF 'Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).' "$S/SKILL.md" \
  && echo "G2 footer OK" || echo "G2 FAIL"

# G3 no personal/home/company paths or names anywhere in the skill folder
grep -rnI -e '/Users/' -e 'C:\\' -e '~/.claude' -e '~/.codex' \
          -e '<company>' -e '<company>' -e '<company>' "$S" && echo "G3 FAIL: leak above" || echo "G3 OK"

# G4 markdown only (no scripts/binaries/tool-config in the skill folder)
find "$S" -type f ! -name '*.md' && echo "G4 FAIL: non-md file above" || echo "G4 OK"

# G5 whole-repo hygiene + (once AIS-004 lands) registry sync
bash init.sh
```

---

# AIS-002 — Migrate & convert skills (spec §7)

**Interfaces produced for AIS-004:** six skill folders under `skills/`, each with a `SKILL.md`
carrying valid `name`/`description` frontmatter and the standard footer — this is exactly what
`tools/gen_registry.py` scans.

Tasks are ordered easiest → hardest (audit ranking) so early commits de-risk the pattern.

### Task 1: Convert `self-review` (easiest — pattern-setter)

**Files:**
- Create: `skills/self-review/SKILL.md` (from `~/.claude/commands/self-review.md`, ~132 lines)

- [ ] **Step 1** — Copy source content into `skills/self-review/SKILL.md`.
- [ ] **Step 2** — Add/normalize frontmatter at the very top:

  ```yaml
  ---
  name: self-review
  description: Review your own branch changes against project standards, quality, cross-file
    consistency, and test coverage; present issues as a table, then auto-fix on request.
  ---
  ```

- [ ] **Step 3** — Neutralize the 3 Claude-Code tool-name mentions (audit `self-review.md:26,100,114`):
  `use Read tool` → "read the file"; `use AskUserQuestion` → "ask the user"; `using Edit tool`
  → "edit the file". Leave the React/jest/vitest/pytest examples (they read as generic examples).
- [ ] **Step 4** — Append the standard footer (Global Constraints) verbatim at end of file.
- [ ] **Step 5** — Run the per-skill verification gate with `S=skills/self-review`. Expected: G1–G4 OK.
- [ ] **Step 6** — Commit:

  ```bash
  git add skills/self-review/SKILL.md
  git commit -m "feat(skills): add self-review (converted from command, neutralized)"
  # include Co-Authored-By trailers for human + AI
  ```

### Task 2: Convert `commit`

**Files:**
- Create: `skills/commit/SKILL.md` (from `~/.claude/commands/commit.md`, ~103 lines)

- [ ] **Step 1** — Copy source; add frontmatter:

  ```yaml
  ---
  name: commit
  description: Create a git commit — derive the ticket id from the branch name, run the
    project's lint gate, optionally group atomic commits, and confirm the message first.
  ---
  ```

- [ ] **Step 2** — Generalize the hardcoded lint gate (audit `commit.md:13-15`, `make lint` /
  `make lint-fix` / "(Biome)") into a discovery ladder, e.g.: "run the project's lint/format
  command if one exists — discover it from the repo (`package.json` scripts, `Makefile`,
  `pyproject.toml`, `.pre-commit-config.yaml`); skip if none."
- [ ] **Step 3** — Swap tool names: `AskUserQuestion or notify_user tool` (`commit.md:54`) →
  "ask the user".
- [ ] **Step 4** — **Resolve the co-author contradiction (Decision #3):** delete the
  `commit.md:103` line "Do not add Co-Authored-By: Claude" and replace with guidance to credit
  all co-authors (human + AI) via `Co-Authored-By` trailers, consistent with the footer.
- [ ] **Step 5** — Append standard footer verbatim.
- [ ] **Step 6** — Verification gate, `S=skills/commit`. Expected G1–G4 OK.
- [ ] **Step 7** — Commit (`feat(skills): add commit (neutralized; co-author rule aligned)`).

### Task 3: Convert `enhance`

**Files:**
- Create: `skills/enhance/SKILL.md` (from `~/.claude/commands/enhance.md`, ~189 lines)

- [ ] **Step 1** — Copy source; add frontmatter:

  ```yaml
  ---
  name: enhance
  description: Turn a rough prompt into a detailed, context-rich prompt — classify intent,
    research project context and codebase, and emit a copy-paste-ready enhanced prompt.
  ---
  ```

- [ ] **Step 2** — Replace `$ARGUMENTS` (`enhance.md:11`, a Claude-Code slash-command variable)
  with neutral phrasing: "the user's rough prompt (the text they provide with this skill)".
- [ ] **Step 3** — Neutralize tool names: `Grep`/`Glob` (`enhance.md:59-60`) → "search the
  codebase"; `AskUserQuestion tool` (`enhance.md:166`) → "ask the user". Keep the multi-tool
  context list (`.cursorrules`, `.github/copilot-instructions.md`, `CLAUDE.md`, `AGENTS.md`) —
  it is already cross-tool and neutral.
- [ ] **Step 4** — Append standard footer verbatim.
- [ ] **Step 5** — Verification gate, `S=skills/enhance`. Expected G1–G4 OK.
- [ ] **Step 6** — Commit (`feat(skills): add enhance (neutralized)`).

### Task 4: Convert `pr` (has the company-URL blocker)

**Files:**
- Create: `skills/pr/SKILL.md` (from `~/.claude/commands/pr.md`, ~72 lines)

- [ ] **Step 1** — Copy source; add frontmatter:

  ```yaml
  ---
  name: pr
  description: Open or update a pull request — detect the ticket and base branch, create the
    PR, optionally link it on the issue tracker, and produce a shareable review summary.
  ---
  ```

- [ ] **Step 2** — **Remove the company leak (Decision #2):** delete the hardcoded
  `issue tracker: https://<issue-tracker-host>/browse/TICKET-ID` (`pr.md:60`). Replace with a generic
  "link the PR on your issue tracker (use the tracker URL configured for this project)".
- [ ] **Step 3** — Genericize the coupled flow: issue-tracker MCP tools (`pr.md:45`) → "if an
  issue-tracker integration is available, comment the PR link on the ticket"; "team chat-ready
  message" (`pr.md:54,62`) → "a review summary you can paste into your team's chat";
  `gh pr create … --squash/--web` (`pr.md:38-40`) → keep `gh` as an *example* mechanism but
  phrase as "create the PR (e.g. via the GitHub CLI or web UI)"; `AskUserQuestion` → "ask the user".
- [ ] **Step 4** — Append standard footer verbatim.
- [ ] **Step 5** — Verification gate, `S=skills/pr`. **G3 must show OK** (confirms the
  `<company>` domain is gone). Expected G1–G4 OK.
- [ ] **Step 6** — Commit (`feat(skills): add pr (removed company URL; tracker/chat genericized)`).

### Task 5: Migrate `cli-subagents` (inline the watchdog)

**Files:**
- Create: `skills/cli-subagents/SKILL.md` (from `~/.claude/skills/cli-subagents/SKILL.md`)
- Create: `skills/cli-subagents/references/codex.md`, `skills/cli-subagents/references/gemini.md`
- Drop (do NOT copy): `scripts/watchdog.sh`

- [ ] **Step 1** — Copy `SKILL.md` and the two `references/*.md`. Frontmatter already has
  `name`/`description` — keep, but soften the description so named CLIs read as examples:
  "…locally installed CLI coding agents (e.g. Codex CLI, Gemini CLI)…".
- [ ] **Step 2** — **Inline the watchdog (Decision #4):** replace the `scripts/watchdog.sh`
  reference in `SKILL.md` with a fenced ```bash block containing the watchdog logic (poll the
  delegate's output file every ~30s; kill on output stall ~600s or hard cap ~2700s; exclude
  self/parent from the pgrep match) so an agent can recreate it inline. Do not ship the `.sh`.
- [ ] **Step 3** — Confirm the discovery ladder stays primary (`command -v` → `npm ls -g` →
  `brew list` → `find /Applications`, audit `SKILL.md:29-31`); ensure Codex/Gemini/`npm`
  specifics read as examples layered on the neutral method, not requirements.
- [ ] **Step 4** — In `references/codex.md`, remove the tilde path
  `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*.jsonl` (`codex.md:41`) → describe generically
  ("the CLI's session/rollout log directory") so G3 passes.
- [ ] **Step 5** — Append the standard footer to `SKILL.md`.
- [ ] **Step 6** — Verification gate, `S=skills/cli-subagents`. **G4 will list the two
  `references/*.md` — that is allowed** (they are markdown); confirm no `.sh` remains. G3 must
  be OK (tilde path gone).
- [ ] **Step 7** — Commit (`feat(skills): add cli-subagents (watchdog inlined; paths neutralized)`).

### Task 6: Migrate `init-harness` (heaviest neutralization)

**Files:**
- Create: `skills/init-harness/SKILL.md` (~589 lines) + `claude-md.md`, `agents-md.md`,
  `init-sh.md`, `settings-json.md`

- [ ] **Step 1** — Copy all five markdown files (already policy-clean: no scripts, no leaks).
  Keep the existing `name`/`description` frontmatter on `SKILL.md`.
- [ ] **Step 2** — **Reframe around a discovery ladder (Decision #5):** where the skill
  targets `.claude/settings.json`, PreToolUse hooks, and `CLAUDE.md` as *the* destinations,
  restate them as "this runtime's settings/hooks file and global-instructions file — discover
  it (Claude Code → `.claude/settings.json` + `CLAUDE.md`; other tools → their equivalent)".
  Keep the concrete Claude-Code artifacts as the worked example. `agents-md.md` already models
  the neutral counterpart — cite it.
- [ ] **Step 3** — Sanity-check external links (`SKILL.md:10,562-588`): they are public
  (github.com/anthropic.com/openai.com), not company-internal — keep, but they are fine to
  trim if stale. No leaks to remove.
- [ ] **Step 4** — Append the standard footer to `SKILL.md`.
- [ ] **Step 5** — Verification gate, `S=skills/init-harness`. G4 lists the four support
  `.md` files (allowed). G3 must be OK.
- [ ] **Step 6** — Commit (`feat(skills): add init-harness (reframed around runtime discovery ladder)`).

### Task 7: AIS-002 acceptance sweep

- [ ] **Step 1** — Run `bash init.sh`; confirm the `skills/` personal-path scan is clean
  (no INFO "skills/ not created").
- [ ] **Step 2** — Confirm all six skills pass G1–G4:

  ```bash
  for S in skills/*/; do echo "== $S =="; \
    head -12 "$S/SKILL.md" | grep -qE '^name:' && head -12 "$S/SKILL.md" | grep -qE '^description:' && echo "fm OK"; \
    grep -qF 'Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).' "$S/SKILL.md" && echo "footer OK"; \
    grep -rnI -e '/Users/' -e '~/.claude' -e '~/.codex' -e '<company>' "$S" || echo "no-leak OK"; \
    find "$S" -type f ! -name '*.md' | grep . && echo "NON-MD PRESENT (review)" || echo "md-only OK"; \
  done
  ```

- [ ] **Step 3** — Update `harness/notes/AIS-002.md`: record the deferral of xlsx-safe-export,
  the `pr`/`commit` fixes, and any surprises. Set AIS-002 `done` in
  `harness/feature_list.json` and `harness/progress.md` **only after** every skill passes.
  Add the AIS-011 (xlsx-safe-export decision) feature entry per Decision #1.

---

# AIS-003 — README protocol (INSTALL / UPDATE)

**Interfaces produced:** `README.md` (the protocol AI agents read in UC1/UC2) and a minimal
`CONTRIBUTING.md` stub so footer/README links resolve. Consumed by AIS-004's UC1 acceptance.

### Task 8: Write `README.md`

**Files:**
- Create: `README.md` (root)

- [ ] **Step 1** — Write **"What is this"** (§5): one paragraph (public registry of AI-neutral,
  markdown-only skills) + "what a good skill looks like" (frontmatter + discovery ladders +
  standard footer, no scripts).
- [ ] **Step 2** — Write **"INSTALL (for AI agents)"** as a UC1 checklist (§3 UC1): read
  `registry.json` → pick a skill → raw-fetch only that skill's folder → place it in *your*
  tool's skills dir (discovery ladder, not a hardcoded path) → write `.provenance.json`
  (schema §4.2, with `commit_sha` from the GitHub API) → append the publish-line to your
  tool's global-instructions file (append only · show the user first · never touch existing
  content). End with **Verify:** skill is in the tool's own dir · provenance is valid JSON ·
  report every check to the user (§5, §6.1).
- [ ] **Step 3** — Include the **publish-line verbatim** for agents to copy (§4.4):

  ```
  After creating any new skill, ask the user whether to publish it
  to https://github.com/AuttapOnG/ai-skills (see its README for the protocol).
  ```

- [ ] **Step 4** — Write **"UPDATE (for AI agents)"** as a UC2 checklist (§3 UC2): read each
  installed `.provenance.json` → check the latest commit SHA per `skill_path` via the GitHub
  API (no clone) → **always show the commit log between installed and latest SHA before
  overwriting** → apply only on user confirmation → if `local_modified: true`, STOP and ask
  the 3-way (keep mine / take upstream / show diff). State intent + pass criteria; let the
  agent pick the mechanism (curl / gh / WebFetch).
- [ ] **Step 5** — Write **"EDIT & CONTRIBUTE"**: brief, pointing to `CONTRIBUTING.md`
  (expanded in Phase 2/AIS-006).
- [ ] **Step 6** — Verify no `<you>` placeholders remain and no personal paths:

  ```bash
  grep -nF '<you>' README.md && echo "FAIL: placeholder" || echo "no-placeholder OK"
  grep -nI -e '/Users/' -e '~/.claude' README.md && echo "review" || echo "no-personal-path OK"
  ```

- [ ] **Step 7** — Commit (`docs: add README install/update protocol for AI agents`).

### Task 9: Add minimal `CONTRIBUTING.md` stub (Decision #6)

**Files:**
- Create: `CONTRIBUTING.md` (root)

- [ ] **Step 1** — One short section: markdown-only policy · offer to contribute improvements
  back (owner pushes / others fork+PR) · `Co-Authored-By` required · "full review checklist +
  branch protection land in AIS-006." Keep it deliberately minimal.
- [ ] **Step 2** — Verify no leaks (`grep -nI -e '/Users/' -e '<company>' CONTRIBUTING.md`).
- [ ] **Step 3** — Update `harness/notes/AIS-003.md`; set AIS-003 `done` after Tasks 8–9 verify.
- [ ] **Step 4** — Commit (`docs: add minimal CONTRIBUTING stub (expanded in AIS-006)`).

---

# AIS-004 — Registry generator + first `registry.json` + UC1 acceptance

**Interfaces consumed:** the six skill folders (AIS-002) and `README.md` (AIS-003).
**Interfaces produced:** `tools/gen_registry.py` (CLI: `--write` regenerates `registry.json`;
`--check` exits non-zero on drift), `registry.json`, and a wired `init.sh` registry-sync check.

### Task 10: Write the registry generator

**Files:**
- Create: `tools/gen_registry.py` (Python 3 stdlib only — no new deps)

- [ ] **Step 1** — Implement a minimal frontmatter reader (stdlib only): for each
  `skills/*/SKILL.md`, read the block between the first two `---` lines, parse simple
  `key: value` pairs (handle a value that wraps onto indented continuation lines), and pull
  `name` + `description`. Fail loudly if either is missing (this doubles as a lint).
- [ ] **Step 2** — Build the registry object per **§4.1**: top-level `generated_at`
  (ISO-8601 UTC) + `skills[]` of `{name, description, path: "skills/<dir>", updated}`.
  `updated` = the last-commit date for that path (`git log -1 --format=%cs -- <path>`),
  falling back to today if git is unavailable. Sort skills by `name` for stable diffs.
- [ ] **Step 3** — CLI contract:
  - `python3 tools/gen_registry.py --write` → write `registry.json` (pretty, trailing newline).
  - `python3 tools/gen_registry.py --check` → regenerate in memory, compare to the committed
    `registry.json` **ignoring the `generated_at` field**, exit 0 if equal else 1 (prints diff).
- [ ] **Step 4** — Manual test on the six skills:

  ```bash
  python3 tools/gen_registry.py --write
  python3 -c "import json;d=json.load(open('registry.json'));print(len(d['skills']),'skills');[print(s['name'],'->',s['path']) for s in d['skills']]"
  ```

  Expected: `6 skills` and each `name -> skills/<name>` line; every `description` non-empty.
- [ ] **Step 5** — Commit (`feat(tools): add gen_registry.py (frontmatter -> registry.json)`).

### Task 11: Generate the first `registry.json`

**Files:**
- Create: `registry.json` (root, generated)

- [ ] **Step 1** — `python3 tools/gen_registry.py --write`.
- [ ] **Step 2** — Validate it is well-formed JSON and matches folders exactly:

  ```bash
  python3 -c "import json;json.load(open('registry.json'))" && echo "valid JSON"
  python3 tools/gen_registry.py --check && echo "in sync"
  ```

- [ ] **Step 3** — Commit (`chore: generate first registry.json (6 skills)`).

### Task 12: Wire `init.sh` registry-sync check

**Files:**
- Modify: `init.sh` (the "Registry sync" section that currently prints
  `INFO: registry.json not created yet`)

- [ ] **Step 1** — Replace the INFO stub: if `registry.json` and `tools/gen_registry.py` both
  exist, run `python3 tools/gen_registry.py --check` and surface PASS/FAIL (non-fatal warning
  vs. clear FAIL line, matching init.sh's existing style). Keep the "not created yet" INFO as
  the fallback when the files are absent.
- [ ] **Step 2** — Test both states:

  ```bash
  bash init.sh    # expect: registry sync PASS
  # (temporarily edit a description, re-run, expect FAIL, then revert)
  ```

- [ ] **Step 3** — Commit (`chore: wire init.sh registry-sync check to gen_registry.py`).

### Task 13: UC1 acceptance — real install on this machine (spec §8 Phase 1 acceptance)

> This is the phase gate. It requires the repo content to be live on GitHub, so it includes an
> **ask-first push checkpoint.**

- [ ] **Step 1** — Pre-push review: `git status`, `git log --oneline origin/main..HEAD`, and a
  final leak sweep across all staged files. Summarize exactly what will go public.
- [ ] **Step 2** — **CHECKPOINT: request explicit human approval to push** (public repo = a
  release; the `.claude/settings.json` PreToolUse hook also blocks `git push` until approved).
- [ ] **Step 3** — After approval, push `main` to `origin`.
- [ ] **Step 4** — Perform a **real UC1 install with Claude Code on this machine**, following
  `README.md` exactly: pick one skill (e.g. `self-review`) from `registry.json`, raw-fetch only
  that folder, place it in the tool's own skills dir (use a scratch/test dir to avoid clobbering
  the live `~/.claude/skills` originals — spec §7 says back up before any real replacement),
  write `.provenance.json`, and (dry-run / show-only) the publish-line append.
- [ ] **Step 5** — Run the README **Verify** checklist and confirm: skill landed in the tool's
  own dir · `.provenance.json` is valid JSON with a real `commit_sha` · every check reported.
- [ ] **Step 6** — Record the full run (commands, output, pass/fail per check) in
  `harness/notes/AIS-004.md`. This is the acceptance evidence per §6.1.
- [ ] **Step 7** — Set AIS-004 `done` (and Phase 1 complete) in `harness/feature_list.json` and
  `harness/progress.md` only after the verify checklist passes end-to-end.

---

## Self-Review — spec coverage

Checked this plan against the spec with fresh eyes:

- **§7 migration table** — cli-subagents ✓(T5), init-harness ✓(T6), commit/pr/self-review/enhance
  ✓(T1–4), worklog → AIS-009 (out of Phase 1, correct), update-tags → local-forever (correct),
  **xlsx-safe-export → deferred to AIS-011 with rationale (Decision #1, T7 step 3).** Gap made
  explicit, not silent.
- **§4.1 registry.json generated** — T10–T11 (generator + first file), never hand-edited ✓.
- **§4.2 .provenance.json** — written during UC1 acceptance T13; schema referenced in README T8 ✓.
- **§4.3 frontmatter + footer** — every skill task adds both; gates G1/G2 enforce ✓.
- **§4.4 publish-line verbatim** — README T8 step 3 ✓.
- **§5 README outline** — all five sections mapped to T8 steps 1–5 ✓.
- **§6.1 verification checklists reported** — per-skill gate + README Verify + T13 ✓.
- **§6.2 markdown-only / no company paths** — gates G3/G4 + init.sh ✓; watchdog.sh & the
  `.py`/`.yaml` handled (T5, Decision #1).
- **§6.3 CI validate.yml** — Phase 2 (AIS-007), intentionally out of scope; init.sh is the
  Phase-1 local stand-in (T12).
- **§8 Phase 1 acceptance** ("install skills from the repo with Claude Code succeeds per verify
  checklist") — T13 ✓.
- **Open question repo name** — resolved (`ai-skills`), reflected in Global Constraints ✓.

No unresolved placeholders. Type/interface names consistent (`gen_registry.py --write/--check`,
gate IDs G1–G5, `.provenance.json` fields per §4.2) across tasks.

## Execution Handoff

After you approve this plan, two execution options:

1. **Subagent-Driven (recommended)** — a fresh subagent per task with review between tasks;
   fast iteration and clean context per skill.
2. **Inline Execution** — I execute tasks in this session with checkpoints for your review.

Either way, AIS-002 → AIS-003 → AIS-004 run in order, and I stop at the Task 13 push checkpoint
for your explicit approval before anything goes public.
