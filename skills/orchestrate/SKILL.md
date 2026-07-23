---
name: orchestrate
description: Turn the main session into a cost-optimized dispatcher — decompose the request, route each task to the cheapest subagent tier that can do it, keep each agent's context minimal, and dispatch one at a time unless the user trades cost for speed. Use ONLY when the user explicitly asks — "orchestrate", "route by cost/difficulty", "use the cheapest model that can handle it", "minimize tokens" — never proactively.
---

# Orchestrate — cost-optimized subagent routing

## Why this exists

Token cost is roughly **(active context size) × (number of turns) × (per-token
price)**. The main session usually runs on the most expensive tier, so every
file it reads and every turn it grinds through is billed at the top rate.
This skill turns the main session into a **dispatcher**: it keeps the
judgment work, and farms reading and execution out to the cheapest capable
tier with the smallest context that still suffices.

Two independent levers follow from the formula — pull both:

- **Difficulty → cheapest capable tier.** Easy work should never run on the
  expensive tier.
- **Context volume → cheap tiers and minimal briefs.** A task can be *easy
  but heavy* (search a whole repo, scan logs). Reading is cheap work — route
  it down regardless of how smart the final answer must be. This lever
  usually saves more than tier choice alone.

## Step 1: Discover your tiers

Do not assume any particular model lineup. Discover, in order:

1. What subagent or delegation mechanism does your runtime offer, and can it
   pin a model per dispatch? (Check your tool's agent/task facilities.)
2. Which model tiers can this account actually use? Requesting an
   unavailable tier is typically rejected, not downgraded — never emit one.
3. If unsure what exists, ask the user once, then cap the routing table at
   the highest tier they confirm.

*(Example only: in Claude Code the tiers might be Haiku / Sonnet / Opus,
selected via a model option on its subagent tool. Other runtimes name and
select tiers differently.)*

With only one tier available, tier routing is moot — the context-volume
lever (briefs, recon, return contract) still applies in full.

## Core rules

1. **Decompose first.** List the tasks. For each, note reasoning difficulty,
   context footprint (how much it must read), files touched, dependencies.
2. **Route by cheapest-capable.** Default down, not up. Exception —
   **expensive-to-redo work** (large generation, destructive refactor):
   classify up front; paying a cheap failed attempt plus a full redo costs
   more than starting on the right tier.
3. **Distill before you escalate.** Never hand raw bulk to the expensive
   tier (see the recon pattern below).
4. **Minimal brief per agent.** Task, relevant paths, constraints — not the
   conversation history.
5. **Enforce the return contract** (below) on every dispatch.
6. **Don't over-dispatch.** A trivial one-file edit is cheaper done inline
   than shipped out — each spawn pays a fresh system prompt.
7. **State the plan first.** One line per task — task → tier → order — so
   the user can veto before tokens are spent.

## Routing table

Route on the **higher** of the two axes (difficulty, footprint):

| Class | Signals | Route to |
|---|---|---|
| Trivial | one file, mechanical, quick lookup | inline in the main session, or lowest tier |
| Easy | bounded edit, clear spec, grep-and-collate | lowest tier |
| Medium | one module, clear requirements, tests, routine refactor | middle tier |
| Hard | architecture, ambiguous spec, cross-cutting or security-sensitive | highest available tier — over a distilled brief, never the raw repo |

**Footprint override:** easy-or-medium reasoning that must read a lot
(repo-wide search, log scan, "find every use of X") goes to the **lowest**
tier, which returns only distilled findings.

**Tie-break:** when torn between tiers, take the cheaper one — unless the
expensive-to-redo exception applies.

## Recon → Distill → Decide

For hard or high-footprint tasks:

1. **Recon (lowest tier):** locate the relevant files, functions, call
   sites; return a brief — paths, key snippets, a one-paragraph summary.
2. **Distill:** the brief is hundreds of tokens, not tens of thousands.
3. **Decide (highest tier):** reason over the brief only.

The smart tier *thinks*; the cheap tier *reads*. The volume cut is the main
win and holds whatever your provider's current price ratios are — check
those rather than assuming them; output tokens typically cost several times
input tokens.

## Return contract

Every dispatched agent returns **only**: files changed with a 1–3 line
summary each · status (done / partial / blocked) · the single blocker, if
any. Explicitly forbid pasting full file contents, narrating process, or
echoing unchanged code. The agent's scratch context must never flow back —
only this summary does.

## Serial by default — parallel by consent

Dispatch **one agent at a time**: await each summary, then re-check the
queue and drop or narrow tasks the result made redundant (**prune-first
ordering** — run uncertainty-resolving tasks first; this re-check is where
serial mode actually saves tokens). One active context at a time also keeps
peak usage low, and back-to-back same-type dispatches can reuse any prompt
caching your runtime does — keep agent instructions stable, put the
per-task brief last.

Serial is a cost posture, not a law: if the user says **speed matters
more**, fan independent tasks out in parallel per your runtime's own
guidance. Say which mode you are using.

**Serial ≠ one agent for everything.** Do not funnel many substantial tasks
into one long-lived agent — its context accrues and is re-billed every
turn. One isolated dispatch per context-heavy task; only trivial items may
be batched.

## When NOT to use

- A single simple task — orchestration overhead exceeds the savings.
- Uniformly hard, small-footprint work — run it on the top tier directly.
- Tightly coupled tasks sharing lots of state — rehydrating context across
  agents costs more than staying in the main session.
- The user asked for delegation to an *external* CLI agent — that is a
  different skill (e.g. cli-subagents), which moves work off this runtime's
  quota entirely; this skill optimizes spend *within* it.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
