---
id: "106"
title: "Mail Manager Dictionary Mails Fix"
status: done
priority: 1
sprint: beta
category: CLIENT
description: "Fix MailManager crash when Nakama returns mails as a dictionary instead of an array."
modified: 2026-06-23
---

### Goal / Risk

Fix `MailManager.fetch_mails()` crash when Nakama returns mail data as a `Dictionary` instead of an `Array`.

Runtime error:

```text
Trying to assign value of type 'Dictionary' to a variable of type 'Array'.
mail_manager.gd:32 @ fetch_mails()
```

### Solution

- Added type guards around `payload.mails` before assigning to typed `mails: Array`.
- Converted dictionary-shaped mail payloads with `.values()`.
- Added safe fallback to `[]` for invalid mail payloads.
- Added type guards for inbox `state`, `claimed_ids`, and `read_ids`.

### Files Modified

- `scripts/managers/mail_manager.gd`

### Verification

- Ran `godot --headless --path "/home/beng/Godot/Projects/tekton-enet" --check-only --quit`.
- Script check completed without parse/type errors.
- Remaining output was unrelated Steam-not-running warning and exit leak noise.

### Acceptance Criteria

- [x] `fetch_mails()` accepts `payload.mails` as `Array`.
- [x] `fetch_mails()` accepts `payload.mails` as `Dictionary`.
- [x] Invalid or missing mail/state data falls back safely.
- [x] Mail sorting and unread count update still run after normalization.
