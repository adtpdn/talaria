---
title: "Chat Storage Admin Tab (Manual Message Browser and Deletion)"
id: "100"
status: done
priority: 02
sprint: beta
category: ADMIN
description: "Add Chat Storage admin tab to list and selectively delete individual channel messages."
modified: "2026-06-19"
---
### Goal / Risk

Admins needed a way to browse and selectively delete individual chat messages from Nakama storage, beyond bulk wipe/purge.

### Solution

- Added 2 backend RPCs: admin_list_channel_messages (paginated), admin_delete_channel_message
- New Chat Storage tab (index 7) with channel ID input, message tree, refresh/pagination, delete selected
- Full wiring in admin_panel.gd: load, paginate, delete with confirmation

### Acceptance Criteria

- [x] Chat Storage tab visible at index 7 in admin panel
- [x] Enter channel ID and Load to fetch messages
- [x] Messages displayed in tree (sender, content, date, ID)
- [x] Refresh button loads next page of older messages
- [x] Delete Selected button removes individual message after confirmation
- [x] Tree updates after deletion
