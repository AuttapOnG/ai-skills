---
name: worklog
description: Scan git logs plus AI-assistant session logs across your repos and create dated worklog entries in your notes system (Notion shown as the example). Supports a "sweep" mode to find date gaps and fill missing entries.
---

Create dated worklog entries by scanning git commits plus AI-assistant session logs.

## Configure

Set or adapt these values before running the workflow:

- `REPOS_ROOT` — directory holding your git repos. The git scan loops over `"$REPOS_ROOT"/*/`.
- `GIT_AUTHOR` — git author name used to filter commits.
- AI session-log locations — directories used by your assistant. For example, Claude may use `~/.claude/projects`; Codex may use `~/.codex` and `~/.codex/sessions`. Substitute the paths and parsers for other assistants.
- `PROJECT_PATH_PREFIX` — optional common parent path used to derive short project labels from session metadata. If it is unset or does not match, the scripts use the last path segment.
- `TZ_OFFSET_HOURS` — UTC offset used to bucket sessions by local date. Set the constant at the top of each Python script.
- Notes system — destination for dated worklog entries. The workflow below uses Notion as an example; set `<YOUR_WORKLOG_DATASOURCE_ID>` to your worklog database or data-source ID, or substitute another notes system.
- Ticket pattern and `<YOUR_PROJECT_TAG>` — replace `PROJ-1234` / `PROJ-XXXX` with your issue-tracker prefix and set the project label stored with each entry.

## Arguments

The user provides a date, date range, or mode as argument: $ARGUMENTS

Examples:
- `2026-04-03` — single day
- `2026-04-01 2026-04-03` — range (inclusive)
- `today` — today only
- `yesterday` — yesterday only
- `sweep` — scan all configured AI-assistant sessions, compare against the notes system, list gaps, and fill missing entries
- *(no argument)* — default to yesterday

## Mode: sweep

When the argument is `sweep` (or user asks to "กวาด" / scan for gaps):

1. Extract all dates and summaries from the configured AI-assistant session logs (see the examples in Steps 3b and 3c)
2. Fetch all existing worklog entries from the notes system (see Step 5)
3. Show the user a diff table of dates found in assistant logs but missing from the notes system
4. Ask the user to confirm before creating missing entries
5. Create the missing entries

---

## Steps

### 1. Parse dates

**IMPORTANT:** Never calculate dates manually — always use the `date` command.

```bash
# Resolve relative dates:
# yesterday   → date -j -v-1d +%Y-%m-%d
# today       → date +%Y-%m-%d
# last friday → date -j -vlast-fri +%Y-%m-%d  (macOS)
```

For `sweep` mode, skip this step (scan all time).

---

### 2. Scan git logs (skip in sweep mode if no commits found)

```bash
for dir in "$REPOS_ROOT"/*/; do
  if [ -d "$dir/.git" ]; then
    repo=$(basename "$dir")
    git -C "$dir" log --author="$GIT_AUTHOR" --since="<START_DATE>" --until="<END_DATE_PLUS_1>" --pretty=format:"$repo|%as|%s" 2>/dev/null
  fi
done
```

Note: `--until` is exclusive, so add 1 day to the end date.

---

### 3a. Format git commits into daily summaries

Group commits by date. For each date:
- Combine related commits (multiple fixes on same feature → one bullet)
- Include ticket IDs (for example, `PROJ-1234`) if present
- Prefix with repo name if commits span multiple repos (e.g., "webapp: ..., rbac-service: ...")
- Keep under ~200 chars

---

### 3b. Example: scan Claude session logs

If Claude is one of the configured assistants, run this Python example in sweep mode and use it to supplement sparse git data otherwise:

```python
import json, os, glob, re
from datetime import datetime, timezone, timedelta
from collections import defaultdict

TZ_OFFSET_HOURS = 7  # set to your UTC offset
PROJECT_PATH_PREFIX = os.path.expanduser(os.environ.get("PROJECT_PATH_PREFIX", ""))
projects_dir = os.path.expanduser("~/.claude/projects")

def clean_msg(text):
    text = re.sub(r'<[^>]+>.*?</[^>]+>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()[:150]

def friendly_project(proj_dir):
    if PROJECT_PATH_PREFIX:
        encoded_prefix = PROJECT_PATH_PREFIX.replace(os.sep, "-").rstrip("-") + "-"
        if proj_dir.startswith(encoded_prefix):
            name = proj_dir[len(encoded_prefix):].split("-", 1)[0]
            return name or "repo"
    return proj_dir.rstrip("-").rsplit("-", 1)[-1] or "Home"

by_date = defaultdict(list)

for proj_dir in sorted(os.listdir(projects_dir)):
    proj_path = os.path.join(projects_dir, proj_dir)
    proj_name = friendly_project(proj_dir)

    for jsonl_file in sorted(glob.glob(os.path.join(proj_path, "*.jsonl"))):
        ai_title = None
        first_user_msg = None
        first_ts = None

        try:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        etype = entry.get('type', '')
                        ts_str = entry.get('timestamp', '')

                        if etype == 'ai-title':
                            ai_title = entry.get('aiTitle', '')

                        if etype == 'user' and first_user_msg is None and ts_str:
                            ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                            first_ts = ts
                            msg = entry.get('message', {})
                            content = msg.get('content', '')
                            if isinstance(content, list):
                                for item in content:
                                    if isinstance(item, dict) and item.get('type') == 'text':
                                        cleaned = clean_msg(item.get('text', ''))
                                        if cleaned:
                                            first_user_msg = cleaned
                                        break
                            elif isinstance(content, str):
                                first_user_msg = clean_msg(content)
                    except:
                        pass
        except:
            pass

        if first_ts and (first_user_msg or ai_title):
            local_time = first_ts + timedelta(hours=TZ_OFFSET_HOURS)
            date_key = local_time.strftime('%Y-%m-%d')
            by_date[date_key].append({
                'proj': proj_name,
                'title': ai_title or '',
                'first_msg': first_user_msg or '',
                'time': local_time.strftime('%H:%M'),
            })

# Deduplicate and print
for date in sorted(by_date.keys()):
    sessions = sorted(by_date[date], key=lambda x: x['time'])
    seen = set()
    unique = []
    for s in sessions:
        key = (s['proj'], s['title'])
        if key not in seen:
            seen.add(key)
            unique.append(s)
    print(f"DATE:{date}")
    for s in unique:
        label = s['title'] or s['first_msg'][:80]
        # skip pure admin/meta sessions
        if label.lower() in ['', 'check claude usage logs for worklog', 'review yesterday\'s work log'] or 'worklog' in label.lower():
            continue
        print(f"  [{s['proj']}] {label}")
    print()
```

This prints dates and session titles for this example assistant. Adapt the location and parser for other assistants.

---

### 3c. Example: scan Codex session logs

If Codex is one of the configured assistants, run this Python example in sweep mode and use it to supplement sparse git data otherwise:

```python
import json, os, glob
from datetime import datetime, timedelta
from collections import defaultdict

TZ_OFFSET_HOURS = 7  # set to your UTC offset
PROJECT_PATH_PREFIX = os.path.expanduser(os.environ.get("PROJECT_PATH_PREFIX", ""))
codex_dir = os.path.expanduser("~/.codex")
index_file = os.path.join(codex_dir, "session_index.jsonl")
session_patterns = [
    os.path.join(codex_dir, "sessions", "**", "*.jsonl"),
    os.path.join(codex_dir, "archived_sessions", "*.jsonl"),
]

titles = {}
try:
    with open(index_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("id") and entry.get("thread_name"):
                    titles[entry["id"]] = entry["thread_name"]
            except:
                pass
except:
    pass

def friendly_project(cwd):
    if PROJECT_PATH_PREFIX:
        try:
            relative = os.path.relpath(cwd, PROJECT_PATH_PREFIX)
            if relative != os.pardir and not relative.startswith(os.pardir + os.sep):
                return relative.split(os.sep, 1)[0] or "repo"
        except ValueError:
            pass
    return os.path.basename(cwd.rstrip("/")) or "Home"

by_date = defaultdict(list)
seen_ids = set()

for pattern in session_patterns:
    for jsonl_file in sorted(glob.glob(pattern, recursive=True)):
        try:
            with open(jsonl_file, "r", encoding="utf-8") as f:
                first = json.loads(f.readline())
            if first.get("type") != "session_meta":
                continue
            payload = first.get("payload", {})
            session_id = payload.get("id", "")
            if not session_id or session_id in seen_ids:
                continue
            seen_ids.add(session_id)
            label = titles.get(session_id, "")
            if not label or "worklog" in label.lower():
                continue
            ts_str = payload.get("timestamp", "") or first.get("timestamp", "")
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            local_time = ts + timedelta(hours=TZ_OFFSET_HOURS)
            by_date[local_time.strftime("%Y-%m-%d")].append({
                "proj": friendly_project(payload.get("cwd", "")),
                "label": label,
                "time": local_time.strftime("%H:%M"),
            })
        except:
            pass

for date in sorted(by_date.keys()):
    print(f"DATE:{date}")
    seen = set()
    for s in sorted(by_date[date], key=lambda x: x["time"]):
        key = (s["proj"], s["label"])
        if key in seen:
            continue
        seen.add(key)
        print(f"  [Codex:{s['proj']}] {s['label']}")
    print()
```

This example scans active and archived sessions for that assistant, deduplicates by session ID, and uses thread names as concise work topics. Adapt the location and parser for other assistants.

---

### 4. Merge sources

For each date, combine git commit summaries plus the configured AI-assistant session titles into one cohesive Entry string. Rules:
- Git commits are ground truth for what was shipped (include ticket IDs)
- Assistant sessions fill in research, review, planning, and POC work not captured in git
- Deduplicate overlapping topics across both assistants
- Skip worklog-administration sessions from both assistants
- Format: `[PROJ-XXXX] <shipped work>; <research/planning topics>`

---

### 5. Check existing notes entries (Notion example)

Fetch all existing Work Log entries to find which dates already have entries.

For the Notion example, search the Work Log database or data source (`<YOUR_WORKLOG_DATASOURCE_ID>`) for recent entries. For each result, fetch the page to get its `date:Date:start` property. Substitute the equivalent query for another notes system.

Build a set of dates that are already covered in Notion.

---

### 6. Show gap diff (required before creating)

Show the user a table of dates that are in the scan results but NOT in Notion:

```
❌ Missing from Notion:
| Date       | Proposed Entry                          | Hours |
|------------|-----------------------------------------|-------|
| 2026-05-07 | Review MCP registry POC; scorecard...   | 8     |
| 2026-05-08 | Fix RBAC tests; PR; cross-tenant MCP... | 8     |

✅ Already in Notion (skipping):
| Date       | Existing Entry                          |
|------------|-----------------------------------------|
| 2026-04-27 | UC3 testing: bot payment happy path...  |
```

**Always ask for confirmation before creating entries.**

---

### 7. Create Notion entries

After confirmation, create pages in the Work Log data source:
- **data_source_id**: `<YOUR_WORKLOG_DATASOURCE_ID>`
- **Entry** (title): formatted summary
- **date:Date:start**: ISO date string
- **date:Date:is_datetime**: 0
- **Project**: `<YOUR_PROJECT_TAG>`
- **Hours**: 8 by default; 4 for half-days (half-day heuristic: only 1-2 combined assistant sessions and activity ends before noon or starts after noon)

---

### 8. Report

Show a final summary table of what was created vs skipped.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
