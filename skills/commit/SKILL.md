---
name: commit
description: Create a git commit — derive the ticket id from the branch name, run the project's lint gate, optionally group atomic commits, and confirm the message first.
---

Create a git commit with the following requirements:

1. Extract the ticket ID from the current branch name (e.g., AAF-31 from feat/AAF-31-streaming-callback)
   - Branch pattern: `<type>/<TICKET-ID>-<description>` or `<TICKET-ID>-<description>`
   - Extract the ticket ID (e.g., AAF-31, AAF-4, etc.)

2. **Run lint and format verification** before proceeding:
   - Run the project's lint/format command if one exists — discover it from the repo (`package.json` scripts, `Makefile`, `pyproject.toml`, `.pre-commit-config.yaml`); skip if none.
   - If lint fails:
     a. Try the project's discovered lint/format auto-fix command first, if one exists
     b. If still failing, show the errors and ask user whether to:
        - "Fix issues" - Let AI attempt to fix the code
        - "Proceed anyway" - Skip lint and continue with commit
        - "Cancel" - Stop the commit process
   - If lint passes, proceed to the next step

3. Check git status and git diff to see what changes will be committed

3.5. **Atomic Commit Strategy** (if multiple file types changed):
   - Analyze changed files and group them by logical changes:
     * **Core changes**: source code, configs, dependencies
     * **Tests**: test files, test configs
     * **Documentation**: README, CLAUDE.md, agent files, comments
     * **Refactoring**: code improvements without functionality changes
     * **Fixes**: bug fixes separate from features

   - If multiple groups exist, ask user:
     * "Single commit" - Commit all changes together (default)
     * "Atomic commits" - Create separate commits per logical group
     * "Custom grouping" - Let me choose which files go together

   - For atomic commits:
     * Create commit message for each group
     * Stage and commit each group separately
     * Maintain logical order (core → tests → docs)

4. Create a commit message with format: `[TICKET-ID] <description>`
   - Example: `[AAF-31] Add streaming callback support`
   - The description should be clear and concise, describing what was changed

5. If no ticket ID is found in the branch name, ask the user whether to:
   - Provide a ticket ID manually
   - Proceed without a ticket ID prefix

6. Follow git best practices:
   - Use imperative mood ("Add feature" not "Added feature")
   - Keep the first line under 72 characters when possible
   - Add detailed description in commit body if needed

7. After creating the commit message, ask the user to review it with the following options:
   - "Yes, commit this" (Recommended) - Proceed with the commit
   - "Modify message" - Let me edit the commit message
   - "Cancel" - Don't commit

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
