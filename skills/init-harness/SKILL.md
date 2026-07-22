---
name: init-harness
description: Use when initializing or upgrading a harness engineering scaffold in the current project — empty repos and projects with existing code, docs, or a partial harness alike. Surveys what exists, then creates or updates CLAUDE.md, AGENTS.md, init.sh, .claude/settings.json, and the harness/ work-control memory (feature_list.json, progress.md, per-feature notes).
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

---

## Step 3: Generate Harness Files

Using the answers from Step 2, generate the files below. Read the supporting template files in this skill directory for the content of each artifact.

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

### Files to Generate

Generate each file, substituting user answers into [PLACEHOLDERS]:

1. **`CLAUDE.md`** (or your runtime's equivalent) — use claude-md.md template, autonomy variant from Q4, substitute Q1/Q2/Q3 answers
2. **`AGENTS.md`** — use agents-md.md template, same autonomy variant
3. **`init.sh`** — use init-sh.md template, risk variant from Q6/Q7, make executable
4. **`.claude/settings.json`** (or your runtime's equivalent) — use settings-json.md template, checkpoint hooks from Q5, permission variant from Q6/Q7
5. **`.claude/commands/`** — create empty directory (placeholder for future commands)
6. **`docs/specs/SPEC-TEMPLATE.md`** — spec template (inline below)
7. **`docs/specs/example-spec.md`** — example spec (inline below)
8. **`docs/adr/ADR-TEMPLATE.md`** — ADR template (inline below)
9. **`docs/adr/0001-harness-init.md`** — auto-generated ADR for this initialization
10. **`harness/evals/eval-template.md`** — eval scaffold (inline below)
11. **`harness/evals/README.md`** — eval instructions (inline below)
12. **`harness/traces/otel-stub.yaml`** — OpenTelemetry stub (inline below)
13. **`harness/traces/README.md`** — observability instructions (inline below)
14. **`harness/feature_list.json`** — work-control queue (see Step 4)
15. **`harness/progress.md`** — bounded progress memory (see Step 4)
16. **`harness/notes/<PREFIX>-001.md`** — first feature note (see Step 4)
17. **`harness/README.md`** — update discipline (see Step 4)

Everything harness-related lives under the visible `harness/` directory —
NOT a hidden `.harness/` — because these are working files humans and agents
open constantly (lesson from MarketPlaceProxy: the split caused confusion and
had to be merged).

After generating CLAUDE.md and AGENTS.md from their templates, append the
work-control sections from Step 4 to both.

---

## Inline Templates (Small Static Files)

### docs/specs/SPEC-TEMPLATE.md

```markdown
# Spec: [Feature Name]

**Status:** draft | review | approved | implemented
**Date:** YYYY-MM-DD

## Goal
One sentence: what does this build and why?

## Background
What context does the agent need to understand the request?

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Out of Scope
What this spec explicitly does NOT cover.

## Success Criteria
How will we know this is done and correct?

## Open Questions
- Question 1
```

### docs/specs/example-spec.md

```markdown
# Spec: Add user authentication endpoint

**Status:** approved
**Date:** 2026-06-30

## Goal
Add a POST /auth/login endpoint that accepts email + password and returns a JWT token.

## Background
The app currently has no authentication. Users are identified by session only.
The agent should not modify any existing endpoints or database schema.

## Requirements
- [ ] POST /auth/login accepts { email, password }
- [ ] Returns { token, expiresAt } on success
- [ ] Returns 401 on invalid credentials
- [ ] Token expires in 24 hours

## Out of Scope
- Registration endpoint
- Password reset
- OAuth / social login

## Success Criteria
- curl -X POST /auth/login -d '{"email":"test@example.com","password":"secret"}' returns 200 with token
- Invalid password returns 401
- Token validates with jwt.verify()
```

### docs/adr/ADR-TEMPLATE.md

```markdown
# ADR-NNNN: [Decision Title]

**Date:** YYYY-MM-DD
**Status:** proposed | accepted | deprecated | superseded

## Context
What is the situation that requires a decision?

## Decision
What was decided?

## Consequences
What are the positive and negative outcomes of this decision?
```

### harness/evals/eval-template.md

```markdown
# Eval: [Task Name]

**Purpose:** Verify the agent can [specific capability] correctly.

## Setup
```bash
# Commands to set up the test environment
```

## Task Prompt
Give the agent exactly this prompt:
> [Exact prompt text]

## Verifier
Run after the agent claims completion:
```bash
# Deterministic check command
# Expected output or exit code
```

## Pass Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Baseline (no skill)
Without the skill, the agent typically: [describe failure mode]
```

### harness/evals/README.md

```markdown
# Evals

Agent behavior evaluations for this project.

## Running an Eval

1. Set up the environment per the eval's Setup section
2. Give the agent the exact Task Prompt
3. Run the Verifier commands after completion
4. Record pass/fail in the eval file

## Adding Evals

Copy eval-template.md, fill in all sections, commit.
Run the baseline (without any skill) first — document what the agent does wrong.
Then add or update the skill, re-run, verify it now passes.
```

### harness/traces/otel-stub.yaml

```yaml
# OpenTelemetry configuration stub
# Uncomment and configure to enable agent observability
#
# See: https://opentelemetry.io/docs/specs/semconv/gen-ai/
# for GenAI semantic conventions

# exporters:
#   otlp:
#     endpoint: http://localhost:4317
#     protocol: grpc

# service:
#   name: [PROJECT_NAME]-agent
#   version: 0.1.0

# instrumentation:
#   gen_ai:
#     capture_message_content: true   # set false in production with PII
```

### harness/traces/README.md

```markdown
# Traces

Observability configuration for agent sessions.

## Enabling Tracing

1. Edit `otel-stub.yaml` and uncomment the relevant sections
2. Set your OTLP endpoint
3. Set `OTEL_EXPORTER_OTLP_ENDPOINT` env var or configure in `.claude/settings.json`

## What to Instrument

Follow [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/):
- Each tool call → one span
- Each agent turn → one parent span
- Token counts as span attributes

## Warning

Do not enable `capture_message_content: true` in production if the project handles PII.
```

---

## Step 4: Work-Control Layer (harness memory)

This layer is the single source of truth for what is done and what is next.
`<PREFIX>` = the Q9 answer. When the survey (Step 1) found existing work,
seed `feature_list.json` with it: completed work → `done` entries (with
acceptance criteria describing what verifiably exists), in-flight work →
`in_progress`, known next steps → `pending`. Feature 001 is always the
harness initialization itself, status `done`. If a feature_list.json already
exists, preserve its entries and IDs — only append and update statuses.

### harness/feature_list.json

```json
{
  "project": "[PROJECT_NAME]",
  "version": "0.1",
  "product_direction": "[One sentence from Q1/Q2 answers or existing README]",
  "features": [
    {
      "id": "[PREFIX]-001",
      "title": "Create project harness",
      "status": "done",
      "priority": "high",
      "description": "Initialize the harness engineering scaffold and work-control memory.",
      "acceptance_criteria": [
        "CLAUDE.md, AGENTS.md, init.sh, and .claude/settings.json exist with the chosen autonomy rules and checkpoint hooks.",
        "harness/feature_list.json tracks the implementation queue.",
        "harness/progress.md records initial decisions.",
        "docs/adr/0001-harness-init.md records the harness profile."
      ]
    }
  ]
}
```

Feature entry schema: `id`, `title`, `status` (pending | in_progress | done),
`priority` (high | medium | low), `description`, `acceptance_criteria`
(verifiable, concrete), optional `recommended_before` (list of feature IDs
this should precede).

### harness/progress.md

```markdown
# Progress

## Current State

[2-4 lines: where the project stands right now and what is next.]

## Feature index

| ID | Title | Status | Note |
|---|---|---|---|
| [PREFIX]-001 | Create project harness | done | [notes/[PREFIX]-001.md](notes/[PREFIX]-001.md) |

## Cross-cutting decisions & events

- YYYY-MM-DD — [dated, one bullet per decision that affects more than one feature]
```

Exactly these three sections — no per-feature day-by-day detail lives here.

### harness/notes/[PREFIX]-001.md

```markdown
# [PREFIX]-001 — Create project harness

**Status:** done (YYYY-MM-DD)

## Notes

- Harness initialized via /init-harness; profile in docs/adr/0001-harness-init.md.
- [Anything discovered during the Step 1 survey worth remembering.]
```

For every other feature seeded from the survey, create a stub note:

```markdown
# [PREFIX]-NNN — [Title]

**Status:** [status]

Acceptance criteria: harness/feature_list.json ([PREFIX]-NNN).

## Notes

(Record decisions, surprises, and gotchas here while implementing.)
```

### harness/README.md

```markdown
# Harness memory

How agents track and control work in this repo.

## Files

- `feature_list.json` — the implementation queue. Every unit of work is a
  feature with an ID ([PREFIX]-NNN), status (`pending` / `in_progress` /
  `done`), priority, and acceptance criteria. Single source of truth for
  what is done and what is next.
- `progress.md` — slim, bounded memory with exactly three sections:
  **Current State**, **Feature index**, **Cross-cutting decisions & events**.
- `notes/[PREFIX]-NNN.md` — one note file per feature: decisions, gotchas,
  and implementation details, so agents only load what a feature needs.
- `evals/` — agent behavior evaluations. `traces/` — observability stub.

## Update discipline

1. Set a feature `in_progress` in `feature_list.json` before starting it.
2. Record decisions and surprises in `notes/[PREFIX]-NNN.md` as you go.
3. On completion: verify every acceptance criterion, set status `done`,
   update **Current State** and the **Feature index** in `progress.md`.
4. Decisions affecting more than one feature go in **Cross-cutting
   decisions & events** (dated, one bullet each).
5. New work discovered mid-feature becomes a NEW feature entry — never
   silently expand scope.

Environment bootstrap: `bash init.sh`. Specs live in `docs/specs/`;
step-by-step plans in `docs/plans/`.
```

### Sections to append to CLAUDE.md (and, without tool-specific paths, AGENTS.md)

```markdown
## Context & Memory Rules
At the start of every session:
1. Run `bash init.sh`
2. Read `harness/progress.md` (Current State + Feature index)
3. Load the feature you are working on: its entry in
   `harness/feature_list.json` and its note file `harness/notes/[PREFIX]-NNN.md`
4. Load any approved spec from `docs/specs/`

## Work Control (harness memory)
`harness/feature_list.json` is the single source of truth for what is done
and what is next. Follow the update discipline in `harness/README.md`:
- Set a feature `in_progress` before starting; `done` only after every
  acceptance criterion is verified.
- Per-feature details go in `harness/notes/[PREFIX]-NNN.md`; cross-feature
  decisions go in the dated cross-cutting log in `harness/progress.md`.
- New work discovered mid-feature becomes a new feature entry — never
  silently expand scope.

## Feature Workflow
New work follows: spec in `docs/specs/` (approved by the human) → plan in
`docs/plans/` → feature entries in `harness/feature_list.json` → TDD
execution (failing test → minimal code → pass → commit).
```

Merge rules for existing CLAUDE.md / AGENTS.md content:
- Keep all pre-existing content; place the new sections after it.
- When an existing section overlaps semantically with a template section
  (e.g. an existing "Testing" note vs "Self-Verification Checklist", or
  AGENTS.md's templated "Session Start" vs the list above), merge them into
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

## ADR Auto-Generation

For `docs/adr/0001-harness-init.md`, generate content using the user's actual Q&A answers:

```markdown
# ADR-0001: Harness Initialization

**Date:** [today's date]
**Status:** accepted

## Context
This project needed a harness engineering scaffold to make agent work reliable and observable.
The harness was initialized using `/init-harness` based on the following project profile:

- Project type: [Q1 answer]
- Stack: [Q2 answer]
- Team size: [Q3 answer]
- Autonomy level: [Q4 answer]
- Checkpoints: [Q5 answer]
- Environment: [Q6 answer]
- Sensitive data: [Q7 answer]
- Deploy target: [Q8 answer]

## Decision
Initialize a full harness scaffold with [autonomy level] autonomy constraints,
[checkpoint list] checkpoints, and [permission variant] permissions.

## Consequences
- Agents operating in this repo follow CLAUDE.md and AGENTS.md constraints
- init.sh must be run at the start of each session
- All risky actions are gated by settings.json hooks
- Harness can be evolved by editing these files; changes should be recorded as new ADRs
```

---

## Authoritative References

The following resources inform what goes into each generated file:

### Foundations
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — initializer agents, init.sh, self-verification, handoff artifacts
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — task state, evaluator design
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — architectural constraints, repo-local instructions, telemetry
- [Harness Engineering — Thoughtworks](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) — context engineering, architectural constraints, entropy management
- [Skill Issue: Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) — weak results are often harness problems, not model problems

### Context & Memory
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — context window as working memory budget
- [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) — durable, repo-local instructions

### Constraints & Guardrails
- [Beyond permission prompts](https://www.anthropic.com/engineering/claude-code-sandboxing) — sandboxing, policy design
- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — safe, inspectable tool boundaries
- [12 Factor Agents](https://www.humanlayer.dev/blog/12-factor-agents) — explicit prompts, state ownership, pause-resume behavior
- [Mitigating Prompt Injection Attacks](https://openhands.dev/blog/mitigating-prompt-injection-attacks-in-software-agents) — confirmation mode, analyzers, hard policies

### Specs & Workflow
- [AGENTS.md format](https://github.com/agentsmd/agents.md) — portable cross-runtime instruction format
- [GitHub Spec Kit](https://github.com/github/spec-kit) — spec-driven development toolkit
- [12-Factor AgentOps](https://www.12factoragentops.com/) — context discipline, validation, reproducible workflows

### Evals & Observability
- [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — what to measure in agent systems
- [OpenTelemetry Semantic Conventions for GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — portable observability conventions
- [Testing Agent Skills Systematically](https://developers.openai.com/blog/eval-skills/) — JSONL logs, deterministic checks

**Full curated list:** https://github.com/walkinglabs/awesome-harness-engineering

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
