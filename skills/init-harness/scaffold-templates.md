# Scaffold Templates (docs, evals, traces, ADR)

Literal file templates for Step 3 items 6–13 of SKILL.md. Replace [PLACEHOLDERS] with the Q&A answers.

## docs/specs/SPEC-TEMPLATE.md

```markdown
---
status: draft
date: YYYY-MM-DD
---

# Spec: [Feature Name]

Set `status` to draft, review, approved, or implemented — init.sh lists a
spec as active once its frontmatter status becomes approved.

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

## docs/specs/example-spec.md

```markdown
---
status: implemented
date: 2026-06-30
---

# Spec: Add user authentication endpoint

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

## docs/adr/ADR-TEMPLATE.md

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

## harness/evals/eval-template.md

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

## harness/evals/README.md

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

## harness/traces/otel-stub.yaml

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

## harness/traces/README.md

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

## docs/adr/0001-harness-init.md (auto-generated)

Generate content using the user's actual Q&A answers:

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
- Orchestration style: [Q10 answer]

## Decision
Initialize a full harness scaffold with [autonomy level] autonomy constraints,
[checkpoint list] checkpoints, and [permission variant] permissions.

## Consequences
- Agents operating in this repo follow CLAUDE.md and AGENTS.md constraints
- init.sh must be run at the start of each session
- Risky actions matching the chosen checkpoints are gated by settings.json hooks
- Harness can be evolved by editing these files; changes should be recorded as new ADRs
```
