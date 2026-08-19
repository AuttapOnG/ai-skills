# Work-Control Templates (harness memory)

Literal file templates for Step 4 of SKILL.md. Seeding rules and the CLAUDE.md/AGENTS.md merge rules live in SKILL.md. Replace [PLACEHOLDERS] and [PREFIX] with the Q&A answers.

## harness/feature_list.json

```json
{
  "project": "[PROJECT_NAME]",
  "version": "0.1",
  "product_direction": "[One sentence from Q1/Q2 answers or existing README]",
  "groups": {
    "harness": "Stand up and evolve the agent harness"
  },
  "features": [
    {
      "id": "[PREFIX]-001",
      "title": "Create project harness",
      "status": "done",
      "priority": "high",
      "group": "harness",
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
(verifiable, concrete), optional `group` (key into the top-level `groups`
map — a short epic/phase/milestone name, each mapped to a one-line goal),
optional `recommended_before` (list of feature IDs this should precede).

## harness/progress.md

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

## Archived groups

- [group] — [N] features, archived YYYY-MM-DD → archive/feature_list.json
```

Exactly these sections (Archived groups appears once something has been
archived) — no per-feature day-by-day detail lives here.

## harness/notes/[PREFIX]-001.md

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

## harness/README.md

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
- `archive/feature_list.json` — append-only archive of retired feature
  entries (same schema). Active list + archive together are the full
  record; feature IDs are never reused.
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
6. When every feature in a group is `done` and the active list exceeds
   ~20 entries, move that group's entries to `archive/feature_list.json`
   and collapse their Feature-index rows into one line under **Archived
   groups** in `progress.md`. Never move or delete note files.

Environment bootstrap: `bash init.sh`. Specs live in `docs/specs/`;
step-by-step plans in `docs/plans/`.
```

## Sections to append to CLAUDE.md (and, without tool-specific paths, AGENTS.md)

```markdown
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
`docs/plans/` → feature entries in `harness/feature_list.json` →
execution at the verification tier below → commit.

## Verification Tiers
Pick the tier from what the change does to behavior:
- **Changes or adds behavior** → full TDD: failing test first → minimal
  code → pass → commit.
- **Leaves behavior unchanged** (typo, comment, config value, rename,
  refactor covered by existing tests) → no new test; run the existing
  tests covering the touched code before claiming done.
- **Spike / throwaway experiment** → tests optional; code that gets kept
  re-enters the top tier before merge.

During the red-green loop run only the tests for the current feature;
run the full suite once before setting the feature `done`.

## Agent Orchestration
[ORCHESTRATION_RULE — one paragraph chosen by Q10:
cost-optimized → "Route heavy reading, searching, and mechanical work to the
cheapest capable agent tier. Give each subagent a minimal brief; subagents
return conclusions only, never raw file dumps. Dispatch sequentially unless
the human explicitly trades cost for speed."
balanced → "Delegate independent subtasks to subagents in parallel. Match the
tier to task difficulty: cheap tiers for reading and searching, capable tiers
for design and review."
speed-first → "Fan out independent work to subagents in parallel by default;
prefer capable tiers. Cost is secondary to wall-clock time."]
Findings from a subagent that affect the current feature are recorded in its
note (`harness/notes/[PREFIX]-NNN.md`) before the feature is set `done`.
```
