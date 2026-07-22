# init.sh Template

Three variants based on risk level. Pick the matching variant.
After generating init.sh in the project, run: `chmod +x init.sh`

Replace [PROJECT_NAME] and [STACK] with user answers.

---

## PRODUCTION variant (production environment or sensitive data)

```bash
#!/usr/bin/env bash
set -e

echo "=== [PROJECT_NAME] — Agent Session Init ==="
echo "Stack: [STACK]"
echo ""

# 1. Environment validation
echo "--- Checking environment ---"
if [ -f ".env.required" ]; then
  while IFS= read -r var; do
    if [ -z "${!var}" ]; then
      echo "ERROR: Required env var '$var' is not set"
      exit 1
    fi
  done < .env.required
  echo "OK: All required env vars present"
fi

# 2. Secret scanning (never commit secrets)
echo "--- Scanning for accidental secrets ---"
if command -v gitleaks &>/dev/null; then
  gitleaks detect --no-banner 2>/dev/null && echo "OK: No secrets detected" || echo "WARNING: Potential secrets found — review before committing"
else
  echo "INFO: gitleaks not installed — consider adding it for secret scanning"
fi

# 3. Git status
echo "--- Git status ---"
git status --short
UNCOMMITTED=$(git status --short | wc -l | tr -d ' ')
if [ "$UNCOMMITTED" -gt 0 ]; then
  echo "WARNING: $UNCOMMITTED uncommitted change(s) — review before proceeding"
fi

# 4. Load active spec
echo "--- Active specs ---"
if ls docs/specs/*.md 2>/dev/null | head -5 | xargs grep -l "status: approved" 2>/dev/null; then
  echo "Above specs are approved and ready"
else
  echo "No approved specs found — create one in docs/specs/ before starting"
fi

echo ""
echo "=== Session ready ==="
```

---

## STAGING variant

```bash
#!/usr/bin/env bash
set -e

echo "=== [PROJECT_NAME] — Agent Session Init ==="
echo "Stack: [STACK]"
echo ""

# 1. Environment validation
echo "--- Checking environment ---"
if [ -f ".env.required" ]; then
  while IFS= read -r var; do
    if [ -z "${!var}" ]; then
      echo "WARNING: Env var '$var' is not set"
    fi
  done < .env.required
fi
echo "OK"

# 2. Git status
echo "--- Git status ---"
git status --short
UNCOMMITTED=$(git status --short | wc -l | tr -d ' ')
if [ "$UNCOMMITTED" -gt 0 ]; then
  echo "NOTE: $UNCOMMITTED uncommitted change(s)"
fi

# 3. Load active spec
echo "--- Active specs ---"
ls docs/specs/*.md 2>/dev/null | xargs grep -l "status: approved" 2>/dev/null || echo "No approved specs"

echo ""
echo "=== Session ready ==="
```

---

## EXPERIMENT/LOCAL variant

```bash
#!/usr/bin/env bash

echo "=== [PROJECT_NAME] — Agent Session Init ==="
echo "Stack: [STACK]"
echo ""

# Git status
git status --short 2>/dev/null || echo "Not a git repo"

# Active specs
echo "--- Active specs ---"
ls docs/specs/*.md 2>/dev/null | xargs grep -l "status: approved" 2>/dev/null || echo "None"

echo ""
echo "=== Ready ==="
```
