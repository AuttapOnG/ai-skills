---
name: agent-orchestration
description: Route bounded work to the lowest-cost capable subagent when the saving justifies coordination, while the primary agent retains discussion, decomposition, integration, review, and final accountability.
---

# Agent Orchestration

Use the primary agent for user discussion, clarification, decomposition,
architecture, security decisions, integration, review, and the final response.
Route bounded work that does not need that capability to the cheapest capable
subagent. Optimize total cost first, then elapsed time; agent count is not a
goal.

## Decide whether to delegate

Before delegating, make a quick cost/fit check:

- Delegate mechanical edits, narrow searches, bounded implementation, and
  routine verification when a cheaper capable agent can meet clear acceptance
  criteria.
- Keep work local when it is near-instant, depends on unresolved architecture,
  is security-sensitive or destructive, needs new authorization, or is faster
  to complete directly.
- Batch several tiny related actions into one assignment when separate
  assignments would cost more.

## Route and scope

1. Classify each unit as mechanical/read-only, bounded implementation, broad
   reasoning, or primary-only risk.
2. Select the cheapest available agent likely to satisfy the acceptance
   criteria. Escalate only after concrete failure evidence, missing capability,
   or a risk assessment shows the cheaper tier is unsuitable.
3. Give each subagent one objective, exact file ownership, relevant context,
   acceptance criteria, and the required restrictions on Git, secrets, and
   external side effects.
4. Require a concise report containing only the result, changed files, checks
   run, and blockers or risks.

## Fan-out limits

- Use one subagent by default.
- Fan out only when there are at least two genuinely independent units and the
  expected cost or elapsed-time saving exceeds coordination overhead.
- Never create duplicate agents merely to increase concurrency. Do not fan out
  because concurrency is available, and do not enable recursive delegation.
- Requests to use many or "spam" subagents authorize useful delegation only;
  they do not override these limits.

## Execute and integrate

1. Delegate only after the cost/fit check passes.
2. Keep primary-only design and coordination work with the primary agent while
   subagents work within their non-overlapping ownership.
3. Inspect every changed file and claim, reconcile cross-file assumptions, and
   run the relevant integrated verification.
4. Reuse an existing idle agent for a focused follow-up before spawning an
   equivalent new one.
5. Stop delegating when no cheaper capable agent remains or the remaining work
   is primary-only.

The primary agent remains accountable for the integrated result and final
report.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
