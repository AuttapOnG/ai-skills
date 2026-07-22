---
name: pr
description: Open or update a pull request — detect the ticket and base branch, create the PR, optionally link it on the issue tracker, and produce a shareable review summary.
---

Create a pull request with the following requirements:

1. Extract the ticket ID from the current branch name:
   - Common patterns: `<type>/<TICKET-ID>-<description>`, `<TICKET-ID>-<description>`, `feature/TICKET-123-desc`
   - Support common prefixes: issue-tracker style (AAF-31, PROJ-123), GitHub issues (#42), or any alphanumeric prefix

2. Detect the base branch:
   - Use the target branch the user provides with this skill (e.g. "develop" or "main")
   - If no target branch is specified, auto-detect: `develop` → `main` → `master` (first that exists)

3. Check if the current branch is pushed to remote:
   - Use `git rev-parse --abbrev-ref --symbolic-full-name @{u}` to check upstream
   - If not pushed: Push with `git push -u origin <branch-name>`
   - If pushed but local is ahead: Push with `git push`

4. Check if a PR already exists for the current branch, then create or update the PR, e.g. via the GitHub CLI or web UI.
   - GitHub CLI examples: check with `gh pr list --head <branch-name>`, update with `gh pr edit`, or create with `gh pr create`.

5. Get the commit history and changes to understand what was done:
   - `git log $BASE_BRANCH..HEAD --oneline`
   - `git diff $BASE_BRANCH...HEAD --stat`

6. Create or update the PR with:
   - Title format: `[TICKET-ID] Brief description` (or just description if no ticket found)
   - Body should be **concise** and include:
     - **Key Changes** section with bullet points (max 8-10 items, 1-2 lines each)
     - **Test Plan** (optional — only for significant changes like new features, bug fixes, breaking changes):
       - Keep concise: 2-4 bullet points max
       - Focus on critical test scenarios only
     - Ticket link at the bottom if ticket ID was found
   - **DO NOT include**: verbose implementation details, complete file lists, or unnecessary sections
   - **GitHub CLI example**:
     - `gh pr create --base <branch> --head <current-branch> --title "..." --body "..." --squash`
     - When using this example, do not use the `--web` flag and include `--squash` to enable squash merge.

7. If no ticket ID is found in the branch name, ask the user for the ticket ID or proceed without it.

8. After successfully creating or updating the PR, if a ticket ID was found and an issue-tracker integration is available, comment the PR link on the ticket:
   - If an issue-tracker integration is not available, silently skip this step.
   - If one is available:
     - Check existing comments on the ticket.
     - Check if any existing comment already contains the PR URL
     - **Only add a comment if the PR URL is NOT already mentioned** (prevents duplicates)
     - Comment format: `Pull request: [#PR_NUMBER - PR_TITLE](PR_URL)`
   - If no ticket ID was found, skip this step entirely.

9. After everything is done (PR created/updated and issue-tracker comment added when available), output **a review summary you can paste into your team's chat** inside a fenced code block (` ```text `):
   ```text
   <polite one-liner asking for review — vary each time, keep it friendly and natural, may include emoji>

   **[TICKET-ID] PR Title**
   PR: <PR_URL>
   Ticket: <ticket-url>
   ```
   - **CRITICAL**: The message MUST be wrapped in a ` ```text ` code fence so it displays as raw text, not rendered markdown. This allows easy copy-paste into the team's chat.
   - The opening line should be a **polite, natural request for review** — do NOT reuse the same phrase every time. Vary the tone and wording (e.g., "Would appreciate your eyes on this 👀", "Mind taking a look? 🙏", "Ready for review, thanks in advance! 🙇").
   - After the opening line, add a **fun quote or programming joke** (1 line) — must be **original and unique every time**, can be Thai or English, relatable to developers. Do NOT reuse jokes from previous conversations. Be creative!
   - If no issue-tracker ticket was found, omit the issue-tracker line.

IMPORTANT:
- Before creating the PR, ask the user to review the proposed title and description with these options:
  - "Yes, create/update PR" (Recommended) - Proceed
  - "Modify PR details" - Let user edit
  - "Cancel" - Don't create/update
- Do NOT add "Generated with Claude Code" or any similar attribution to the PR description.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
