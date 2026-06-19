# Task: Chat Storage Admin Tab (Manual Message Browser and Deletion)

**Status:** Done
**Date:** 2026-06-19

## Problem
Admins needed a way to browse and selectively delete individual chat messages from Nakama storage, beyond the bulk wipe and purge in the Lobby Chat tab. There was no UI to list or delete specific messages.

## Changes

### server/nakama/lua/admin.lua
- rpc_admin_list_channel_messages: paginated list of messages in any channel (returns message_id, sender_id, username, content, create_time, next_cursor)
- rpc_admin_delete_channel_message: delete a single message by channel_id and message_id
- Both registered as RPCs with admin role guard

### scripts/services/backend_service.gd
- admin_list_channel_messages(channel_id, limit, cursor, forward): typed wrapper
- admin_delete_channel_message(channel_id, message_id): typed wrapper

### scenes/ui/admin_panel.tscn
- New Chat Storage tab (index 7) with:
  - Channel ID input and Load button
  - Message Tree (columns: Sender, Content, Date, ID)
  - Refresh button (loads next page of older messages)
  - Delete Selected button

### scripts/ui/admin_panel.gd
- Added onready refs for all new nodes
- Added state vars: _chat_tree_root, _chat_channel_id, _chat_cursor, _chat_messages_data
- Tab setup: ChatTree columns configured (Sender, Content, Date, ID)
- _on_load_chat_messages: clears tree, fetches first page (50 msgs, reverse-chronological)
- _fetch_chat_messages_batch: fetches page, appends rows, shows cursor for pagination
- _on_delete_chat_message: confirmation dialog, delete via RPC, remove from tree
- Auto-loads when tab 7 is selected

## How to use
1. F10, Chat Storage tab
2. Paste channel ID into input, click Load
3. Messages appear (sender, content, date, ID)
4. Click Refresh to load older messages (paginated)
5. Select a message, Delete Selected, confirm, done
