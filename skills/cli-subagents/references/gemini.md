# Gemini CLI (Google)

> Status: NOT yet verified on this machine — Gemini CLI was not installed as
> of 2026-07-10. Before first real use, verify the flags below against
> `gemini --help` and update this file with what you observe (the Codex file
> is the model for what to record: dispatch command, sandbox behavior,
> monitoring signals).

## Locating the binary
- `command -v gemini` (npm global: `npm i -g @google/gemini-cli`).

## Dispatch command (verify before use)

```bash
gemini --yolo -p "<prompt>" </dev/null
```

Run as a background task; capture stdout to the task output file (no pipes).

- `-p/--prompt` = non-interactive one-shot mode.
- `--yolo` = auto-approve all tool actions (the equivalent of Codex
  `--full-auto`). Without it, headless runs stall waiting for approvals.
- `--sandbox` exists for containerized execution; check what it requires
  locally before relying on it.
- Same universal rule: close stdin with `</dev/null` — assume any agent CLI
  may read stdin.

## Things to verify on first use, then document here
- Does it respect the CWD as the workspace? Any trust prompt on first run
  in a new directory?
- Network access policy in whatever sandbox mode you use.
- Whether it can run git commits.
- Where its session/debug logs live (for the hung-vs-busy diagnosis).
