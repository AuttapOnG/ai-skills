# Eval: init-harness — converge an existing project without clobbering it

**Purpose:** Verify the agent can upgrade a project that already has a CLAUDE.md and a partial harness — preserving all existing content, entries, and IDs instead of blind-overwriting.

## Setup
```bash
mkdir -p /tmp/ih-converge && cd /tmp/ih-converge && git init -b main -q
cat > CLAUDE.md <<'EOF'
# Legacy Project
MARKER-KEEP-ME: never build on Fridays.
## Testing
Run `make test` before any commit.
EOF
mkdir -p harness
cat > harness/feature_list.json <<'EOF'
{"project":"Legacy","version":"0.1","features":[
 {"id":"LG-001","title":"Ship v1 API","status":"done"},
 {"id":"LG-002","title":"Add rate limiting","status":"in_progress"}]}
EOF
printf 'legacy\n' > README.md && git add -A && git commit -qm "seed"
```

## Task Prompt
Give the agent exactly this prompt:
> /init-harness
Accept all inferred answers; Q4 = medium; Q5 = never.

## Verifier
Run after the agent claims completion:
```bash
cd /tmp/ih-converge
# 1. pre-existing content preserved
grep -q "MARKER-KEEP-ME" CLAUDE.md || exit 1
# 2. existing feature IDs and statuses preserved (append-only)
jq -e '.features[] | select(.id=="LG-001" and .status=="done")' harness/feature_list.json >/dev/null || exit 1
jq -e '.features[] | select(.id=="LG-002" and .status=="in_progress")' harness/feature_list.json >/dev/null || exit 1
jq -e '.features | length >= 3' harness/feature_list.json >/dev/null || exit 1
# 3. overlapping sections merged, not duplicated
[ "$(grep -c '^## Verification Tiers' CLAUDE.md)" -le 1 ] || exit 1
[ "$(grep -c '^## Context & Memory Rules' CLAUDE.md)" -le 1 ] || exit 1
# 4. the existing "make test" convention folded in, not deleted
grep -q "make test" CLAUDE.md || exit 1
echo PASS
```

## Pass Criteria
- [ ] Verifier exits with PASS
- [ ] New harness feature (LG-003 or next free ID) records the upgrade itself
- [ ] Q5 = never → settings.json has no hooks section

## Baseline (no skill)
Without the skill, the agent typically overwrites CLAUDE.md wholesale (losing project-specific rules like the MARKER line) and regenerates feature_list.json from scratch, destroying existing IDs and in-progress state.
