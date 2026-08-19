---
name: init-harness
description: Use when initializing or upgrading a harness engineering scaffold in the current project — empty repos and projects with existing code, docs, or a partial harness alike, or when a project needs repo-local agent instructions, guardrails, and work-control memory set up.
---

# init-harness

Initialize a full harness engineering scaffold in the current project, following best practices from the harness engineering community.

Targets below use Claude Code's files (`.claude/settings.json`, `CLAUDE.md`) as the worked example; for another runtime, discover its equivalent global-instructions file, settings file, and hooks mechanism and adapt.

**Authoritative source:** https://github.com/walkinglabs/awesome-harness-engineering

---

## Step 1: Survey the Project (always — greenfield or existing)

This skill's job is to CONVERGE the current project onto the full harness,
no matter what already exists. An existing project is not a reason to stop
or to ask permission per file — survey it, then create what is missing and
update what is stale.

1. Read what exists before asking anything:
   - `CLAUDE.md` (or your runtime's equivalent), `AGENTS.md`, `README.md`, `init.sh`, `.claude/settings.json` (or your runtime's equivalent)
   - `harness/` (feature_list.json, progress.md, notes/) and `docs/` (specs, plans, ADRs)
   - package manifests (package.json, pyproject.toml, go.mod, …)
   - `git log --oneline -30` and `git status --short`
2. Classify each harness artifact:
   - **missing** → generate it
   - **exists** → merge: preserve all user/project content, inject only the
     harness sections that are missing or outdated. Never blind-overwrite.
3. Everything you learned feeds later steps: survey findings pre-fill the
   Q&A (Step 2) and seed the feature list (Step 4) — work already completed
   (visible in git history, docs, or code) becomes `done` features; work in
   flight becomes `in_progress`; obvious next steps become `pending`.

---

## Step 2: Interactive Q&A

First, answer as many of the questions below as you can from the Step 1
survey (e.g. stack from the manifest, project type from the code). Present
all inferred answers in ONE confirmation message. Then ask only the
questions that could not be inferred, **one at a time** — do not bundle the
unknowns.

### Project Dimension

**Q1 — Project type:**
> "What type of project is this?"
> - web app (with UI)
> - backend service / API (headless)
> - CLI tool
> - library / SDK
> - data pipeline
> - other (ask them to describe briefly)

**Q2 — Primary stack:**
> "What is the primary language and framework/stack?"
> (Accept free text — e.g. "Python + FastAPI", "TypeScript + Next.js", "Go")

**Q3 — Team size:**
> "What is the team size working on this project?"
> - solo
> - small (2–5 people)
> - large (6+ people)

### Autonomy Dimension

**Q4 — Autonomy level:**
> "How autonomous should the agent be in this project?"
> - **low** — require explicit approval for most actions (safest)
> - **medium** — require approval only for risky or destructive actions
> - **high** — fully autonomous, actions logged for audit

**Q5 — Human checkpoints:**
> "Where do you want mandatory human checkpoints? (you can name multiple)"
> - before deploy / git push
> - before file deletion
> - before external API / network calls
> - never (fully autonomous)

### Risk Dimension

**Q6 — Environment:**
> "What is the primary target environment?"
> - production
> - staging
> - experiment / local only

**Q7 — Sensitive data:**
> "Does this project handle sensitive data?"
> - yes — API keys / secrets
> - yes — PII / personal data
> - no sensitive data

**Q8 — Deploy target:**
> "What is the deploy target?"
> - cloud (AWS / GCP / Azure / etc.)
> - on-premises
> - local only
> - no deployment

**Q9 — Feature ID prefix:**
> "What prefix should feature IDs use? (e.g. MP → MP-001, MP-002)"
> Suggest 2-3 letter initials derived from the project name; accept free text.

### Delegation Dimension

**Q10 — Orchestration style:**
> "When agents delegate work to subagents, what should they optimize for?"
> - **cost-optimized** — cheapest capable tier, minimal briefs, sequential by default
> - **balanced** — parallel where independent, tier matched to task difficulty
> - **speed-first** — parallel fan-out by default, capable tiers freely

---

## Step 3: Generate Harness Files

Using the answers from Step 2, generate the files below. Every artifact's
content lives in a template file in this skill directory — read the one you
need when generating that artifact:

- **claude-md.md** / **agents-md.md** — instruction files, per autonomy variant
- **init-sh.md** — session bootstrap script, per risk variant
- **settings-json.md** — permissions + checkpoint hooks
- **scaffold-templates.md** — docs/specs, docs/adr (incl. the auto-generated init ADR), harness/evals, harness/traces
- **work-control.md** — harness memory files + sections to append to CLAUDE.md/AGENTS.md

### Answer → Variant Mapping

**Autonomy level (Q4) → CLAUDE.md + AGENTS.md variant:**
- `low` → LOW AUTONOMY sections in claude-md.md and agents-md.md
- `medium` → MEDIUM AUTONOMY sections
- `high` → HIGH AUTONOMY sections

**Checkpoints (Q5) → settings.json hooks:**
- "before deploy / git push" → add PreToolUse hook blocking `git push`, `deploy`, `kubectl apply`
- "before file deletion" → add PreToolUse hook blocking `rm`, `rmdir`, `unlink`, `git clean`
- "before external API / network calls" → add PreToolUse hook blocking `curl`, `wget`, `fetch`
- "never" → no hooks (omit hooks section)

**Permissions (Q6 + Q7) → settings.json variant:**
- STRICT if Q6 = production OR Q7 = secrets / PII
- PERMISSIVE only if Q6 = experiment/local AND Q7 = no sensitive data
- MODERATE for all other combinations (staging with any data, or experiment/local with PII)

**Risk level (Q6 + Q7) → init.sh checks:**
- PRODUCTION variant: Q6 = production OR Q7 = secrets / PII (secret scanning + env var validation)
- STAGING variant: Q6 = staging AND Q7 ≠ secrets / PII (env var validation only)
- EXPERIMENT/LOCAL variant: Q6 = experiment/local AND Q7 = no sensitive data (minimal checks)

**Orchestration style (Q10) → "Agent Orchestration" appended section:**
- Q10 selects the [ORCHESTRATION_RULE] paragraph in work-control.md's appended sections.

### Files to Generate

Generate each file, substituting user answers into [PLACEHOLDERS]:

1. **`CLAUDE.md`** (or your runtime's equivalent) — use claude-md.md template, autonomy variant from Q4, substitute Q1/Q2/Q3 answers
2. **`AGENTS.md`** — use agents-md.md template, same autonomy variant
3. **`init.sh`** — use init-sh.md template, risk variant from Q6/Q7, make executable
4. **`.claude/settings.json`** (or your runtime's equivalent) — use settings-json.md template, checkpoint hooks from Q5, permission variant from Q6/Q7
5. **`.claude/commands/.gitkeep`** — placeholder for future commands (git does not track empty directories)
6. **`docs/specs/SPEC-TEMPLATE.md`** — spec template (scaffold-templates.md)
7. **`docs/specs/example-spec.md`** — example spec (scaffold-templates.md)
8. **`docs/adr/ADR-TEMPLATE.md`** — ADR template (scaffold-templates.md)
9. **`docs/adr/0001-harness-init.md`** — ADR for this initialization, auto-generated from the Q&A answers (template in scaffold-templates.md)
10. **`harness/evals/eval-template.md`** — eval scaffold (scaffold-templates.md)
11. **`harness/evals/README.md`** — eval instructions (scaffold-templates.md)
12. **`harness/traces/otel-stub.yaml`** — OpenTelemetry stub (scaffold-templates.md)
13. **`harness/traces/README.md`** — observability instructions (scaffold-templates.md)
14. **`harness/feature_list.json`** — work-control queue (work-control.md; seeding rules in Step 4)
15. **`harness/progress.md`** — bounded progress memory (work-control.md)
16. **`harness/notes/<PREFIX>-001.md`** — first feature note (work-control.md)
17. **`harness/README.md`** — update discipline incl. group archiving (work-control.md)
18. **`docs/plans/.gitkeep`** — placeholder for the step-by-step plans referenced by the Feature Workflow

Everything harness-related lives under the visible `harness/` directory —
NOT a hidden `.harness/` — because these are working files humans and agents
open constantly (lesson from MarketPlaceProxy: the split caused confusion and
had to be merged).

After generating CLAUDE.md and AGENTS.md from their templates, append the
work-control sections from work-control.md to both.

---

## Step 4: Work-Control Layer (harness memory)

This layer is the single source of truth for what is done and what is next.
`<PREFIX>` = the Q9 answer. When the survey (Step 1) found existing work,
seed `feature_list.json` with it: completed work → `done` entries (with
acceptance criteria describing what verifiably exists), in-flight work →
`in_progress`, known next steps → `pending`. Feature 001 is always the
harness initialization itself, status `done`. If a feature_list.json already
exists, preserve its entries and IDs — only append and update statuses.

All literal templates for this layer live in **work-control.md**:
`feature_list.json` (with the feature entry schema and the `groups` map),
`progress.md`, the note files, `harness/README.md` (update discipline
including group archiving), and the sections to append to CLAUDE.md and
AGENTS.md (Work Control, Feature Workflow, Verification Tiers, Agent
Orchestration). Generate from those templates, then apply the merge rules
below.

Merge rules for existing CLAUDE.md / AGENTS.md content:
- Keep all pre-existing content; place the new sections after it.
- When an existing section overlaps semantically with a template section
  (e.g. an existing "Testing" note vs "Self-Verification Checklist", or
  an existing session ritual vs the template's "Session Start"), merge them into
  ONE section — fold the existing project-specific points into the template
  section rather than keeping two competing headings or lists.
- `recommended_before` in feature entries: omit the field entirely unless
  the feature genuinely should precede specific other features.

---

## Step 5: Commit

Finish by committing the scaffold (one commit, message
`chore: initialize harness engineering scaffold` or
`chore: upgrade harness scaffold` when converging an existing project).
Run `bash init.sh` once first to confirm it executes cleanly. If the
project's checkpoint rules gate commits, ask the human instead.

---

## Authoritative References

The curated sources behind each generated file are listed in
**references.md** in this skill directory.
Full list: https://github.com/walkinglabs/awesome-harness-engineering

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
