---
name: skill-updater
description: Use when the user wants to check for or apply updates to skills installed from a shared skills registry, or asks whether the registry has anything new — "update my skills", "are my skills up to date?", "any new skills in the registry?", or any mention of syncing installed skills with their source repo. Inventories every installed skill's .provenance.json, compares against the registry's latest commits via the host's API (no clone), reports skills that are new in the registry but not yet installed, previews the commit log, and applies changes only on confirmation — never overwriting local edits.
---

# Skill Updater

Keeps skills installed from a shared registry (an `ai-skills`-style repo whose README defines
the INSTALL/UPDATE protocol) in sync with upstream. The core promise: **never overwrite
silently** — the user always sees what would change before anything changes.

Provenance is the source of truth. Every registry-installed skill carries a
`.provenance.json` beside its `SKILL.md`:

```json
{
  "source_repo": "https://github.com/<owner>/<repo>",
  "skill_path": "skills/<name>",
  "commit_sha": "<sha it was installed at>",
  "installed_at": "YYYY-MM-DD",
  "local_modified": false
}
```

## Step 1 — Inventory installed skills

Discover where *your* runtime keeps installed skills — do not assume a fixed path; different
tools differ. Try, in order: your own documentation or configuration for a skills directory;
a `skills` directory under your tool's user-level home; the project's skill directory.
(Example: Claude Code keeps user skills in a `skills` folder inside its home directory.)

Then find every `.provenance.json` under that directory. Each one is an updatable skill.
Skills **without** provenance are local-only — leave them alone, but mention them in the
final report so the user knows they were skipped, not missed.

## Step 2 — Check upstream (no clone)

For each skill, ask the source host's API for the latest commit touching its `skill_path`,
and compare with the recorded `commit_sha`. Group calls by `source_repo` — registries may
differ per skill. Example for a GitHub-hosted registry:

```
GET https://api.github.com/repos/<owner>/<repo>/commits?path=<skill_path>&per_page=1
```

- Latest sha == recorded sha → **up-to-date**, skip.
- Different → **behind**, collect it for the preview.
- Path returns no commits / 404 → the skill was **removed or moved upstream** — report it
  and offer: keep the local copy as-is (flip it to local-only by noting so in the report) or
  delete it. Do not delete without an explicit choice.
- API errors or rate limits → report which skills could not be checked; never guess.

## Step 3 — Discover skills new in the registry

Updating only what's installed would miss skills added to the registry since you last looked.
For each distinct `source_repo`, fetch the registry's machine-readable index (e.g.
`registry.json` at the repo root — the registry's README names it). Any entry whose `name`
has no matching folder in your skills directory is **new in the registry**: collect its
`name` + `description` for the preview. Don't install anything yet — new skills are opt-in,
and the user may have deliberately skipped some (a skill absent locally is not a defect).
If the index can't be fetched, say so and continue with updates only.

## Step 4 — Preview before anything changes

For every skill that is behind, show the commits between the installed sha and the latest
(subject + author is enough). List commits **touching the skill's path** and cut the list at
the recorded sha — e.g. on GitHub, `GET /repos/<owner>/<repo>/commits?path=<skill_path>`,
keeping entries until you reach the installed sha. (A repo-wide compare such as
`/compare/<installed>...<latest>` returns *every* commit in the range, most of them unrelated
to this skill — don't show that noise. If the installed sha never appears in the path's
history, show the path's full recent log and say so.) Present one summary table:

| skill | installed | latest | commits behind | note |
|---|---|---|---|---|
| worklog | `ad0a6ae` | `f3c9b12` | 2 | |
| commit | `473579d` | `473579d` | up-to-date | |
| skill-search | — | `f3c9b12` | — | **new in registry** — "find skills by …" |
| my-local-thing | — | — | — | local-only, skipped |

Then ask which to act on: apply all updates, a subset, or none — and separately, which new
skills (if any) to install. **Apply only what the user confirms.**

## Step 5 — Respect local edits

If a skill's provenance has `local_modified: true`, **stop and ask** before touching it —
the user deliberately changed it. Offer exactly three choices:

- **keep mine** — skip the update, leave `local_modified: true`.
- **take upstream** — replace with the registry version, reset `local_modified: false`.
- **show me the diff first** — fetch the upstream files, diff against local, then re-ask.

A locally-improved skill is also a publishing candidate — if the local version looks like an
improvement, mention that it could be contributed back (see the registry's README) rather
than discarded.

## Step 6 — Apply confirmed updates and installs

For each confirmed skill:

1. Raw-fetch every file under its `skill_path` at the latest commit — only that folder,
   not the whole repo (e.g. `https://raw.githubusercontent.com/<owner>/<repo>/<sha>/<path>/...`).
2. Replace the installed folder's contents wholesale — don't merge file-by-file; upstream may
   have renamed or removed files. (For a **new** install there is nothing to replace — this
   is the registry's INSTALL protocol: same fetch, fresh folder.)
3. Write `.provenance.json` with the `commit_sha` fetched, today's date as `installed_at`, and
   `local_modified: false`.

## Step 7 — Verify (report every check to the user)

- [ ] Every provenance-carrying skill was either up-to-date, updated-on-confirmation, or
      explicitly left alone — none silently skipped.
- [ ] No `local_modified` skill was overwritten without an explicit keep/take/diff choice.
- [ ] Each updated or newly-installed skill's `.provenance.json` records the right
      `commit_sha` and is valid JSON.
- [ ] Skills new in the registry were reported (name + description) — installed only on
      explicit confirmation, never auto-installed.
- [ ] Local-only skills were reported as skipped.
- [ ] Anything that could not be checked (API errors, removed paths) was reported, not hidden.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
