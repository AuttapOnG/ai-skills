# settings.json Template

Three permission variants (STRICT / MODERATE / PERMISSIVE) and hook blocks per checkpoint choice.
Assemble the final file by picking the permission variant then appending the relevant hook blocks.

---

## STRICT permissions (production + sensitive data)

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Bash(git status)",
      "Bash(git log*)",
      "Bash(git diff*)"
    ],
    "deny": [
      "Bash(rm*)",
      "Bash(rmdir*)",
      "Bash(git push*)",
      "Bash(curl*)",
      "Bash(wget*)",
      "Bash(npm publish*)",
      "Bash(pip install*)",
      "WebFetch",
      "WebSearch"
    ]
  }
}
```

---

## MODERATE permissions (staging)

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Write",
      "Bash(git*)",
      "Bash(npm*)",
      "Bash(pip*)"
    ],
    "deny": [
      "Bash(rm -rf*)",
      "Bash(git push --force*)",
      "Bash(curl * | bash*)"
    ]
  }
}
```

---

## PERMISSIVE permissions (experiment/local, no sensitive data)

```json
{
  "permissions": {
    "allow": ["*"],
    "deny": [
      "Bash(curl * | bash*)",
      "Bash(wget * | bash*)"
    ]
  }
}
```

---

## Hook blocks (append based on Q5 checkpoint answers)

### "before deploy / git push" hook

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'cmd=$(jq -r \".tool_input.command\"); if echo \"$cmd\" | grep -qE \"git push|deploy|kubectl apply|helm upgrade\"; then echo \"HARNESS: deploy action requires human approval\" >&2; exit 2; fi'"
          }
        ]
      }
    ]
  }
}
```

### "before file deletion" hook

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'cmd=$(jq -r \".tool_input.command\"); if echo \"$cmd\" | grep -qE \"^rm |^rmdir |git clean\"; then echo \"HARNESS: file deletion requires human approval\" >&2; exit 2; fi'"
          }
        ]
      }
    ]
  }
}
```

### "before external API / network calls" hook

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'cmd=$(jq -r \".tool_input.command\"); if echo \"$cmd\" | grep -qE \"^curl |^wget |^fetch \"; then echo \"HARNESS: external network call requires human approval\" >&2; exit 2; fi'"
          }
        ]
      },
      {
        "matcher": "WebFetch",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'HARNESS: WebFetch requires human approval' >&2; exit 2"
          }
        ]
      }
    ]
  }
}
```

---

## Assembly Instructions

1. Start with the permission variant block matching Q6/Q7
2. If Q5 includes any checkpoint, merge the `hooks` key into the JSON
3. If multiple checkpoints are selected, merge the `PreToolUse` arrays together
4. Write the assembled JSON to `.claude/settings.json`
