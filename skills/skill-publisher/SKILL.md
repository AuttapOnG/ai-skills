---
name: skill-publisher
description: Use after creating or substantially improving a skill to offer publishing it to a shared skills registry — ask first, then audit for safety and neutrality, normalize frontmatter and footer, regenerate the registry, and open the change as a push or pull request with co-author credit.
---

# Skill Publisher

Turns a locally-created or edited skill into a clean contribution to a shared, public,
tool-neutral skills registry (for example, an `ai-skills`-style repo whose README defines the
INSTALL/UPDATE/publish protocol). You do the judgment; this skill sequences the steps.

## When to use

- Right after you finish creating a brand-new skill.
- After you make a non-trivial improvement to a skill that carries a "distributed from …"
  footer (an installed registry skill).
- When the user says "publish this skill" / "contribute this back".

## Step 0 — Ask first (never publish silently)

Publishing sends content to a public place. **Always ask the user before doing anything
outward-facing**, and show them what will be published. Some skills are machine- or
org-specific and should stay local — respect a "no".

> "I can publish `<name>` to `<registry>`. Want me to? I'll audit it, normalize it, regenerate
> the registry, and open it as a push (if you own the repo) or a pull request."

If the target registry is unknown, ask which repo. If the user declines, stop — and if this
skill was installed from a registry, set `local_modified: true` in its `.provenance.json` so a
future update won't silently overwrite the local change.

## Step 1 — Audit (reject-or-fix before publishing)

Read the whole skill and confirm it is safe and portable. This is the same bar a reviewer
applies to an incoming contribution:

- [ ] **Markdown only** — one `SKILL.md` (+ optional markdown support files). No executable
  scripts, binaries, or tool-specific config files. Move runnable snippets into fenced code
  blocks.
- [ ] **No secrets / personal / internal data** — no tokens, no absolute or home paths
  (`/Users/…`, `C:\…`, `~/.tool/…`), no company-internal names, URLs, or hostnames.
- [ ] **Tool-neutral** — discovery ladders instead of hardcoded tool names or paths as
  requirements; named tools appear only as clearly-labeled examples.
- [ ] **No dangerous instructions** — nothing that exfiltrates data, reaches outside the
  skill's own scope, hides encoded/obfuscated blobs, or tries to override a host tool's rules
  ("ignore previous instructions" and relatives).

If anything fails, fix it (or ask the user) before continuing. Do not publish a skill that
still contains internal data — public history is effectively permanent.

## Step 2 — Normalize

- [ ] Frontmatter has `name` and `description` (both required; `description` is what the
  registry indexes — make it a crisp one-liner of when to use the skill).
- [ ] The registry's **standard footer** is present verbatim at the end of `SKILL.md` (copy it
  from any existing skill in that registry; do not improvise the wording).
- [ ] The skill lives at the registry's expected path (e.g. `skills/<name>/SKILL.md`).

## Step 3 — Regenerate the registry index

The registry's machine-readable index (e.g. `registry.json`) is **generated, never
hand-edited**. Regenerate it with the repo's own method — discover it (a generator script in a
`tools/` or `scripts/` directory, a Make target, or the instructions in the repo's README /
CONTRIBUTING) and run that. Confirm the new skill now appears and the index validates.

## Step 4 — Publish

- **You own the repo:** commit to a branch and push, or push to the default branch if that's the
  repo's workflow.
- **You don't own it:** fork, branch, and open a pull request; a maintainer reviews and merges.
- Either way, **every commit credits all co-authors (human and AI) via `Co-Authored-By`
  trailers.** Write a clear message: what the skill does and why it's being added/changed.
- Before any push, show the user the exact diff/commit summary and confirm.

## Step 5 — Stamp provenance & verify

- [ ] After the change lands, record/refresh the skill's `.provenance.json` (source repo,
  skill path, the new commit SHA, install date, `local_modified: false`).
- [ ] Confirm and **report every check to the user**: audit passed · frontmatter + footer
  present · registry regenerated and valid · change pushed or PR opened · commits carry
  `Co-Authored-By` · provenance stamped.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
