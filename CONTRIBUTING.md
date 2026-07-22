# Contributing to ai-skills

Thanks for improving a skill or adding a new one. This registry is public and consumed by AI
agents, so contributions are held to a tight, security-conscious bar.

## Ground rules

- **Markdown only.** A skill is one `SKILL.md` plus optional markdown support files. Pull
  requests that add executable scripts (`.sh`, `.py`, …), binaries, or tool-specific config
  files are declined by default. Put runnable snippets in fenced code blocks inside the markdown.
- **Tool-neutral.** No hardcoded absolute or home paths (`/Users/…`, `C:\…`, `~/.tool/…`) as
  requirements; no company-internal names, URLs, or secrets. Use discovery ladders ("find your
  tool's skills directory") and mention specific tools only as clearly-labeled examples.
- **Frontmatter + footer.** Every `SKILL.md` starts with `name` + `description` frontmatter
  (both required — `description` feeds `registry.json`) and ends with the standard footer that
  links back to this repo.
- **`registry.json` is generated** — never hand-edit it. Regenerate with
  `python3 tools/gen_registry.py --write` and commit the result.
- **Credit co-authors.** Every commit must credit all co-authors (human and AI) via
  `Co-Authored-By` trailers.

## How to contribute

- **Repo owner:** commit to a branch and push; `main` is protected (see below).
- **Everyone else:** fork, create a branch, open a pull request. A maintainer reviews and
  approves before merge. Non-owner changes reach `main` only through this path.

## Review checklist (what a reviewer verifies)

- [ ] `SKILL.md` has `name` + `description` frontmatter and the standard footer.
- [ ] Body is tool-neutral (discovery ladders, no hardcoded paths / required tool names).
- [ ] No personal paths, company-internal names/URLs, or secrets.
- [ ] Markdown only — no scripts, binaries, or tool config files.
- [ ] `registry.json` regenerated and in sync (`gen_registry.py --check` passes).
- [ ] Commits carry `Co-Authored-By` trailers.

## Security red flags — reject on sight

Because installed skills are instructions an agent will follow on a user's machine, a PR is
**rejected** (not just changes-requested) if a skill contains any of:

- **Data-exfiltration** instructions — sending files, environment variables, tokens, or command
  output to an external endpoint.
- **Out-of-scope file access** — reading or writing outside the skill's own concern (e.g.
  touching `~/.ssh`, credential stores, or unrelated project files).
- **Encoded/obfuscated blobs** — base64/hex payloads, or "decode and run this" steps.
- **Prompt-injection patterns** — "ignore previous instructions", attempts to override the host
  tool's system prompt or safety rules, or to silently rewrite the user's global config.
- **Network side effects** presented as harmless — curl/wget piped to a shell, silent installs.

When in doubt, ask in the PR before merging. CI (`.github/workflows/validate.yml`) enforces the
mechanical checks (registry sync, frontmatter/footer, no personal paths, markdown-only); the
red-flag review above is a human judgment that CI cannot fully automate.

## Branch protection

`main` requires pull requests with maintainer approval for non-owner changes, and CI must pass.
This keeps a public, agent-consumed registry from accepting unreviewed instructions.
