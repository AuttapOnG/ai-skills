# Codex CLI (OpenAI)

## Locating the binary
Discover it — do not assume an install location:
1. `command -v codex` + `ls -la` the result. A real file or symlink into an
   npm/brew package is trustworthy; a shell *alias* is not (it won't execute
   in non-interactive shells). Verify with `codex --version`.
2. Not on PATH? Check `npm ls -g @openai/codex` and `brew list codex`.
3. Still nothing? Some installs ship the CLI inside a desktop app bundle:
   `find /Applications -maxdepth 4 -name codex 2>/dev/null`.

Always dispatch with the resolved absolute path — background shells may not
source the profile that puts nvm/brew on PATH.

## Dispatch command

```bash
<codex-binary> exec --sandbox workspace-write "<prompt>" </dev/null
```

Run as a background task; capture stdout to the task output file (no pipes).

- `exec` = headless one-shot mode. It prints "Reading additional input from
  stdin..." and will block forever unless stdin is closed — hence `</dev/null`.
- `--sandbox workspace-write` lets it edit files in the workdir plus /tmp.
  (`--full-auto` is a deprecated alias; still works.)
- Codex picks up the current directory as workdir; `cd` to the repo first
  or run with the repo as CWD.

## Sandbox behavior observed (macOS, v0.144)
- **No network.** Pre-install all deps on the host before dispatch.
- **Cannot bind ports** — server/listener tests fail with EPERM. Tell it in
  the plan which test commands to run instead (e.g. a mocha glob excluding
  server tests); the host runs the rest later.
- **`.git` writes may fail.** Tell it: attempt commits, and on failure log
  `- [codex] commit failed for: <message>` to a state file and continue.
- MCP auth errors (`rmcp::transport::worker ... AuthRequired`) at startup
  are noise from its own MCP servers — harmless, ignore.

## Monitoring
- Session logs: the CLI's session/rollout log directory — a new log
  file appears shortly after a healthy start. No new file + ~0 CPU = hung
  (almost always the stdin issue).
- The exec header prints model/sandbox/session id early; if the output file
  is still empty after a couple of minutes, suspect a hang.
