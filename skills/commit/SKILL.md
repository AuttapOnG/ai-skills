---
name: commit
description: Create a git commit using the current repository context, relevant verification, and a concise message without unnecessary confirmation steps.
---

Create a git commit with the following requirements:

1. Extract the ticket ID from the current branch name when one exists (e.g., AAF-31 from feat/AAF-31-streaming-callback)
   - Branch pattern: `<type>/<TICKET-ID>-<description>` or `<TICKET-ID>-<description>`
   - Extract the ticket ID (e.g., AAF-31, AAF-4, etc.)

2. **Run relevant verification** before proceeding:
   - Run only the narrowest project verification relevant to the changed files; discover it from the repo (`package.json` scripts, `Makefile`, `pyproject.toml`, `.pre-commit-config.yaml`). Do not run broad checks by default.
   - If lint fails:
     a. Try the project's discovered lint/format auto-fix command first, if one exists
     b. If still failing, show the errors and ask user whether to:
        - "Fix issues" - Let AI attempt to fix the code
        - "Proceed anyway" - Skip lint and continue with commit
        - "Cancel" - Stop the commit process
   - If lint passes, proceed to the next step

3. Check git status and git diff to see what changes will be committed

3.5. **Atomic Commit Strategy** (only when scope is materially ambiguous or the owner requests it):
   - Analyze changed files and group them by logical changes:
     * **Core changes**: source code, configs, dependencies
     * **Tests**: test files, test configs
     * **Documentation**: README, CLAUDE.md, agent files, comments
     * **Refactoring**: code improvements without functionality changes
     * **Fixes**: bug fixes separate from features

   - Treat the current changes as one commit by default. Do not ask about
     grouping for one coherent change.

   - For atomic commits:
     * Create commit message for each group
     * Stage and commit each group separately
     * Maintain logical order (core → tests → docs)

4. Create a concise commit message. Use `[TICKET-ID] <description>` when a
   ticket ID is available; otherwise omit the ticket prefix.
   - Example: `[AAF-31] Add streaming callback support`
   - The description should be clear and concise, describing what was changed

5. If no ticket ID is found in the branch name and the owner did not provide
   one, omit the ticket prefix. Do not stop to ask for a ticket ID.

6. Follow git best practices:
   - Use imperative mood ("Add feature" not "Added feature")
   - Keep the first line under 72 characters when possible
   - Add detailed description in commit body if needed

7. An explicit request to commit authorizes the commit. After deriving a
   suitable message, stage the intended files and commit without asking for
   redundant confirmation. Ask only when file scope is materially ambiguous or
   a required verification gate fails.

## Atomic Commit Examples

**Example 1: Feature with docs**
```
Commit 1: [AAF-31] Add streaming callback support
- src/services/streaming.ts
- src/types/streaming.ts

Commit 2: [AAF-31] Add tests for streaming callbacks
- testing/services/streaming.test.ts

Commit 3: [AAF-31] Document streaming callback usage
- CLAUDE.md
- README.md
```

**Example 2: Bug fix**
```
Commit 1: [AAF-313] Fix button color rendering issue
- src/components/ui/button.tsx
- src/app/globals.css
- tailwind.config.ts

Commit 2: [AAF-313] Update guidelines to prevent dark mode
- CLAUDE.md
- .claude/agents/*.md
```

## Best Practices for Atomic Commits

✅ **DO:**
- Each commit should be a complete, working change
- Group related files that serve the same purpose
- Keep commits focused on one logical change
- Order commits: core → tests → docs

❌ **DON'T:**
- Mix refactoring with new features
- Combine bug fixes with unrelated changes
- Split a single logical change across commits
- Create commits that break the build

IMPORTANT:
- Do not push to remote unless explicitly requested.
- Credit all co-authors (human and AI) via `Co-Authored-By` trailers.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
