---
name: cli-subagents
description: Delegate implementation work to locally installed CLI coding agents (e.g. Codex CLI, Gemini CLI) running as background subagents, so a written plan executes on their quota while you keep the spec, review, verification, and commit roles.
---

# CLI Subagents — delegate execution to local coding agents

## Why this exists

The coordinating agent's tokens are the scarce resource; executing a
well-written plan is the cheap part. A local CLI agent can execute the plan
on its own quota while the coordinating agent's turn ends (no waiting cost).
The coordinating agent keeps every role that needs judgment.

**Never delegate:** spec + plan authoring, diff review, host-side
verification, git commits/bookkeeping, scope judgment. **Delegate only:**
executing a self-contained plan with explicit steps and code.

## Step 1: Detect what's installed

```bash
# Example discovery for Codex CLI and Gemini CLI.
for c in codex gemini; do command -v "$c" && ls -la "$(command -v "$c")" && "$c" --version; done
```

`command -v` may report a shell *alias* that fails in non-interactive
shells. Resolve to a real executable file, verify it runs with `--version`,
and dispatch with that absolute path — background shells may not source the
user's profile (nvm, brew). If nothing is on PATH, discover instead of
assuming a location: `npm ls -g`, `brew list`, then
`find /Applications -maxdepth 4 -name <cli> 2>/dev/null` (some vendors ship
the CLI inside a desktop app).

Pick one agent per task — prefer the one the user has been using; otherwise
ask once. If none exist, say so and execute the plan yourself — don't
simulate delegation.

Before first use of an agent in a session, read its reference file. For the
included Codex CLI and Gemini CLI examples, see `references/codex.md` and
`references/gemini.md`.

## Step 2: Pre-flight (on host)

Delegates run sandboxed: **no network, may fail writing `.git`, cannot bind
ports**. Before dispatch:

1. Install every dependency the plan needs — the agent cannot fetch.
2. Write the plan as a self-contained checkbox file in the repo (exact
   paths, complete code in every step, exact commands with expected
   output) — the agent sees only that file, not this conversation.
3. Top it with a **Global Constraints** section: commands NOT to run
   (network, publish/push, port-binding tests), what to do when a git
   commit fails (log to a state file, continue), which checkboxes are
   host-only.
4. If your runtime's pre-execution hooks search command strings, keep those literal strings out
   of the plan and the dispatch prompt.

## Step 3: Dispatch as a background task

Non-negotiable mechanics (each learned the hard way):

- **Close stdin with `</dev/null`** — these CLIs otherwise hang forever
  reading stdin (~0 CPU, empty output).
- **Run in background, raw output** — no `tail`/`head` pipes; they hide
  interim output until exit.
- **Start the watchdog immediately** (Step 4).

Keep the prompt short: point at the plan file, say "execute task-by-task,
checking off checkboxes", restate the Global Constraints. Exact syntax per
agent is in its reference file. Embed a **unique token** (e.g.
`task <repo>-<feature>-xyz`) — other instances of the same CLI may be
running; the token lets monitoring target only this run.

## Step 4: Watchdog — always

A hung delegate looks exactly like a busy one. Launch as a second
background task right after dispatch:

There is no shipped script — recreate this watchdog inline when you need it.

```bash
# Watchdog for a delegated CLI-agent background run.
# Kills the agent if its output file stops growing (stall) or exceeds a hard cap.
# Usage: watchdog.sh <output-file> <pgrep-pattern> [stall-secs] [cap-secs]
OUT="$1"; PATTERN="$2"; STALL_LIMIT="${3:-600}"; HARD_CAP="${4:-2700}"; INTERVAL=30
start=$(date +%s); last_size=-1; last_change=$start
find_agent_pid() {
  for p in $(pgrep -f "$PATTERN"); do
    [ "$p" = "$$" ] && continue; [ "$p" = "$PPID" ] && continue
    ps -o command= -p "$p" 2>/dev/null | grep -q "watchdog" && continue
    echo "$p"; return
  done
}
while true; do
  pid=$(find_agent_pid)
  [ -z "$pid" ] && { echo "watchdog: agent gone — normal exit."; exit 0; }
  now=$(date +%s); size=$(wc -c < "$OUT" 2>/dev/null || echo 0)
  [ "$size" != "$last_size" ] && { last_size=$size; last_change=$now; }
  [ $((now-last_change)) -ge "$STALL_LIMIT" ] && { echo "stalled ${STALL_LIMIT}s; killing $pid"; kill "$pid"; exit 2; }
  [ $((now-start)) -ge "$HARD_CAP" ] && { echo "hard cap ${HARD_CAP}s; killing $pid"; kill "$pid"; exit 3; }
  sleep $INTERVAL
done
```

Never a generic pgrep pattern like `codex exec` — it would kill unrelated
runs. Defaults: kill after 10 min without output growth, or 45 min total;
scale both to plan size. Cheap progress checks:
`grep -c '^- \[x\]' <plan>` (anchored), `git status --short`, output file
size.

## Step 5: Verify on host, then own the result

On exit (the harness notifies you): read the output tail + checkboxes + any
failure notes. Review the full diff yourself — the delegate's claims are
not evidence. Re-run ALL verification on the host, especially what the
sandbox couldn't. Make the commits it couldn't, update bookkeeping, and
report — including anything it skipped.

If the watchdog killed it: find where it stalled, fix the cause,
re-dispatch — ticked checkboxes make resume cheap.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
