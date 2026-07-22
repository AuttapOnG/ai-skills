# Evals

Agent behavior evaluations for this project. The Phase 3 test matrix
(UC1–UC4 on both Claude Code and Codex — AIS-010) lives here as eval files.

## Running an Eval

1. Set up the environment per the eval's Setup section
2. Give the agent the exact Task Prompt
3. Run the Verifier commands after completion
4. Record pass/fail in the eval file

## Adding Evals

Copy eval-template.md, fill in all sections, commit.
Run the baseline (without any skill) first — document what the agent does wrong.
Then add or update the skill, re-run, verify it now passes.
