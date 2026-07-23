---
name: handoff
description: Compact the current conversation into a self-contained handoff document a fresh agent can resume from — state, decisions with reasons, pointers to artifacts instead of duplicated content, suggested skills, and a redaction pass. Use when the user wants to end a session, move work to another agent or tool, or says "write a handoff", "summarize for the next session", "prepare a context handover".
---

# Handoff — package this session for the next agent

## Why this exists

A fresh agent starts with zero context. Everything it cannot recover from
the repo, the tracker, or this document is lost work: decisions get
re-litigated, dead ends get re-explored, half-finished changes get
misread. A good handoff makes the next session start where this one
stopped — at the cost of one written page.

## Step 1: Choose where the document lives

Not in the project workspace by default — a handoff is session scratch,
not a project artifact, and committing it pollutes the repo. Discover a
location in this order:

1. A scratch/temp directory your runtime designates for session files.
2. The operating system's temp directory.
3. Only if the user explicitly wants it versioned: the project's own
   notes/docs convention (follow the repo's existing layout).

Tell the user the exact path in your final message.

## Step 2: Write the document

Use this skeleton; drop sections that would be empty rather than padding
them:

```markdown
# Handoff — <one-line goal> (<date>)

## Where things stand
2–5 sentences: what was asked, what is finished (verified how), what is
not. State plainly which claims were tested vs. assumed.

## Decisions made (and why)
One bullet per decision: what was chosen, the reason, and any alternative
that was considered and rejected. This is the section that prevents
re-litigating.

## In flight / next steps
Ordered list. For each: the next concrete action, and anything known that
makes it easier (file paths, commands that work, the failing test name).

## Artifacts — pointers, not copies
Links/paths only: commits, branches, PRs, issues, specs, plans, generated
files. Never paste their content — the next agent can open them, and
copies go stale.

## Environment notes
Gotchas this session paid to learn: auth quirks, commands that hang,
sandbox limits, rate limits, "X must run before Y".

## Suggested skills
Skills the next agent should invoke for this work, with a phrase on when.
Name them only if they are discoverable in the target environment.

## Open questions for the user
Anything blocked on a human decision — stated so the user can answer in
one message.
```

If the user said what the next session will focus on, weight the document
toward that: expand its next steps, trim unrelated history.

## Step 3: Redact

Before saving, sweep the draft for anything that must not travel: API
keys, tokens, passwords, connection strings, personal data, internal
hostnames or company-confidential names if the handoff might leave the
organization. Replace with a placeholder naming where the real value
lives (e.g. `<token — in the usual env var>`).

## Step 4: Verify (report to the user)

- [ ] The fresh-agent test: could an agent with zero context resume from
      this document plus the referenced artifacts alone? If any step
      needs "what we said earlier", the document is not done.
- [ ] No content duplicated from existing artifacts — pointers only.
- [ ] Redaction pass done; no secrets or unexplained internal names.
- [ ] The user was told the file's exact location.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
