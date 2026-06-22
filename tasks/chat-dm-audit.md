---
title: "Audit Chat and Direct Message Systems"
id: "105"
status: done
priority: 03
sprint: beta
category: AUDIT
description: "Reviewed global lobby chat and friend DM systems for bugs after BackendService RPC fix."
modified: "2026-06-22"
---
### Goal / Risk

Ensure the global chat and friend DM systems were not affected by the RPC payload parsing bug, and that no other silent failures existed.

### Solution

- Verified `lobby_chat.gd` uses Nakama socket's `received_channel_message` directly (bypasses the RPC layer), so it was unaffected.
- Verified `friend_manager.gd` DM channels use `ChannelType.DirectMessage` and write to the socket directly.
- Verified `_on_chat_message_received` correctly filters out self-sent messages.
- Verified DM tabs and history fetching work without relying on `BackendService.api_rpc_async`.
- Confirmed no additional bugs found.

### Acceptance Criteria

- [x] Global chat messages send and receive normally.
- [x] Friend DMs (`@username`) open a tab, send, and receive messages.
- [x] DM history loads when opening a tab.
- [x] `/clear` works in DM context only.
