# Eval: init-harness — greenfield init on a non-code, non-git project

**Purpose:** Verify the agent can initialize a complete harness on a project that has no git repo, no manifests, and no test suite — adapting the scaffold instead of assuming a code project.

## Setup
```bash
mkdir -p /tmp/ih-greenfield && cd /tmp/ih-greenfield
printf '<html><body>design canvas placeholder</body></html>' > "My Design.dc.html"
mkdir screenshots && touch screenshots/01-home.png
# no git init, no package manifests, no tests — that is the point
```

## Task Prompt
Give the agent exactly this prompt:
> /init-harness
When asked, answer: Q4 = high; Q5 = "only irreversible git actions — plain file deletion is fine" (free text). Accept all inferred answers.

## Verifier
Run after the agent claims completion:
```bash
cd /tmp/ih-greenfield
# 1. all core artifacts exist
for f in CLAUDE.md AGENTS.md init.sh .claude/settings.json .claude/commands/.gitkeep \
  docs/specs/SPEC-TEMPLATE.md docs/specs/example-spec.md docs/adr/ADR-TEMPLATE.md \
  docs/adr/0001-harness-init.md docs/plans/.gitkeep harness/feature_list.json \
  harness/progress.md harness/README.md; do [ -e "$f" ] || { echo "MISSING $f"; exit 1; }; done
# 2. git repo created with the scaffold committed
git rev-parse HEAD >/dev/null || exit 1
# 3. init.sh runs clean and does NOT false-match template/example specs
bash init.sh | grep -q "None" || exit 1
# 4. settings.json valid; no invalid allow-all glob
jq -e .permissions .claude/settings.json >/dev/null || exit 1
jq -e '.permissions.allow | index("*")' .claude/settings.json >/dev/null && exit 1
# 5. custom Q5 honored: hook blocks destructive git, allows plain rm
CMD=$(jq -r '.hooks.PreToolUse[0].hooks[0].command' .claude/settings.json)
echo '{"tool_input":{"command":"git reset --hard HEAD~1"}}' | bash -c "$CMD" 2>/dev/null; [ $? -eq 2 ] || exit 1
echo '{"tool_input":{"command":"rm old.png"}}' | bash -c "$CMD"; [ $? -eq 0 ] || exit 1
# 6. no-test-suite project: Verification Tiers carries a verification analog
grep -qi "verification analog\|visual" CLAUDE.md || exit 1
echo PASS
```

## Pass Criteria
- [ ] Verifier exits with PASS
- [ ] harness/feature_list.json seeds pre-existing work (the design file) as `done` entries with a `groups` map
- [ ] Exactly one `## Context & Memory Rules` heading in CLAUDE.md (no duplicate sections)

## Baseline (no skill)
Without the skill, the agent typically writes an ad-hoc CLAUDE.md with no work-control memory, no checkpoint hooks, and no session bootstrap. Pre-AIS-027 skill baseline (observed in the 2026-08-19 dogfood run on a real design-canvas project): free-text Q5 answers had no mapping row, non-code projects got a "tests pass" checklist with no test suite to run, and the non-git case had no `git init` step — all three had to be improvised by the executing agent.
