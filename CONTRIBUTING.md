# Contributing to ai-skills

Thanks for improving a skill! This is a minimal guide — the full review checklist and branch
protection land in a later phase.

- **Markdown only.** Skills are `SKILL.md` (+ optional markdown support files). Pull requests
  that add executable scripts, binaries, or tool-specific config files are declined by default.
- **Tool-neutral.** No hardcoded absolute/home paths, no company-internal names or URLs, no
  secrets. Prefer discovery ladders over hardcoded tool names.
- **Frontmatter + footer.** Every `SKILL.md` needs `name` + `description` frontmatter and the
  standard footer that links back to this repo.
- **How to contribute.** The repo owner pushes directly; everyone else forks and opens a PR.
- **Credit co-authors.** Every commit must credit all co-authors (human and AI) via
  `Co-Authored-By` trailers.

> The complete contribute-back protocol (review red-flags, `local_modified` handling, CI
> checks) is expanded in a later phase.
