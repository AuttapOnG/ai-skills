#!/usr/bin/env bash
set -e

echo "=== ai-skills — Agent Session Init ==="
echo "Stack: Markdown + JSON (skills registry, public repo)"
echo ""

# 1. Secret scanning (this repo is public — nothing sensitive may enter)
echo "--- Scanning for accidental secrets ---"
if command -v gitleaks &>/dev/null; then
  gitleaks detect --no-banner 2>/dev/null && echo "OK: No secrets detected" || echo "WARNING: Potential secrets found — review before committing"
else
  echo "INFO: gitleaks not installed — consider adding it for secret scanning"
fi

# 2. Personal/internal path scan (skills must be portable and public-safe)
echo "--- Scanning skills/ for personal paths ---"
if [ -d "skills" ]; then
  # Generic patterns are public-safe. Company-specific terms live in a git-ignored
  # local file (.scan-local-patterns, one term per line) so the scan stays effective
  # without hardcoding internal names in this public repo.
  SCAN_PATTERN='/Users/|C:\\\\'
  if [ -f ".scan-local-patterns" ]; then
    EXTRA=$(grep -vE '^[[:space:]]*(#|$)' .scan-local-patterns | paste -sd '|' -)
    [ -n "$EXTRA" ] && SCAN_PATTERN="$SCAN_PATTERN|$EXTRA"
  fi
  HITS=$(grep -rlE "$SCAN_PATTERN" skills/ 2>/dev/null || true)
  if [ -n "$HITS" ]; then
    echo "WARNING: personal/internal references found in:"
    echo "$HITS"
  else
    echo "OK: skills/ clean"
  fi
else
  echo "INFO: skills/ not created yet (Phase 1 pending)"
fi

# 3. Registry sync check (registry.json is generated — must match skills/ frontmatter)
echo "--- Registry sync ---"
if [ -f "registry.json" ] && [ -d "skills" ]; then
  if [ -f "tools/gen_registry.py" ] && command -v python3 >/dev/null 2>&1; then
    # Authoritative check: regenerate from frontmatter and diff (ignores generated_at)
    if ! python3 tools/gen_registry.py --check; then
      echo "WARNING: registry.json out of sync — run: python3 tools/gen_registry.py --write"
    fi
  else
    # Fallback when the generator or python3 is unavailable: crude count comparison
    FOLDERS=$(find skills -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
    ENTRIES=$(grep -c '"name"' registry.json || true)
    if [ "$FOLDERS" = "$ENTRIES" ]; then
      echo "OK: registry entries ($ENTRIES) match skill folders ($FOLDERS)"
    else
      echo "WARNING: registry entries ($ENTRIES) != skill folders ($FOLDERS) — regenerate registry.json"
    fi
  fi
else
  echo "INFO: registry.json not created yet (Phase 1 pending)"
fi

# 3b. Skill <-> harness parity (every skill must be tracked by the work-control memory)
#     A skill can land via any path (a merged PR, a direct commit) without a feature entry —
#     which is exactly how it drifts. Word-boundary grep across ALL of harness/ (not just
#     feature_list.json) so batch features that name their skills only in a note still count.
echo "--- Skill/harness parity ---"
if [ -d "skills" ] && [ -f "harness/feature_list.json" ]; then
  UNTRACKED=""
  for d in skills/*/; do
    [ -d "$d" ] || continue
    n=$(basename "$d")
    grep -rqw "$n" harness/ 2>/dev/null || UNTRACKED="$UNTRACKED $n"
  done
  if [ -n "$UNTRACKED" ]; then
    echo "WARNING: skill(s) not referenced anywhere in harness/ — add a feature entry (see harness/README.md):"
    for n in $UNTRACKED; do echo "  - $n"; done
  else
    echo "OK: every skill is tracked in harness/"
  fi
else
  echo "INFO: skills/ or harness/feature_list.json missing — parity check skipped"
fi

# 4. Git status
echo "--- Git status ---"
git status --short
UNCOMMITTED=$(git status --short | wc -l | tr -d ' ')
if [ "$UNCOMMITTED" -gt 0 ]; then
  echo "WARNING: $UNCOMMITTED uncommitted change(s) — review before proceeding"
fi

# 5. Active spec pointer
echo "--- Specs (docs/specs/) ---"
ls docs/specs/*.md 2>/dev/null || echo "No specs found"

echo ""
echo "=== Session ready — read harness/progress.md next ==="
