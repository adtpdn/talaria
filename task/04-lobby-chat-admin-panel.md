# Lobby Chat Admin Panel (Config + Wipe + Purge)

**Status:** Done

## Context
The admin panel had no controls for lobby chat. Admins needed to: set a system prefix, control how many messages load on join, wipe the entire chat, and purge old messages.

## Changes

### `server/nakama/lua/utils.lua`
- Added `utils.SYSTEM_USER_ID` constant (`"00000000-0000-0000-0000-000000000000"`)

### `server/nakama/lua/admin.lua`
- `rpc_admin_get_chat_config` — reads config from Nakama storage (`config/lobby_chat`)
- `rpc_admin_set_chat_config` — writes prefix, max_messages, max_age_days to storage
- `rpc_admin_purge_old_messages` — deletes messages older than N days from a channel
- All 3 registered as RPCs with admin role guard

### `scripts/services/backend_service.gd`
- Added typed wrapper methods: `admin_get_chat_config()`, `admin_set_chat_config(config)`, `admin_purge_old_messages(channel_id, max_age_days)`

### `scenes/ui/admin_panel.tscn`
- New **"Lobby Chat"** tab (index 6) with:
  - System Prefix input (LineEdit)
  - Max messages loaded spinner (10-200, default 50)
  - Delete messages older than spinner (0-365 days)
  - Wipe Chat / Purge Old / Save Config buttons
  - Status label

### `scripts/ui/admin_panel.gd`
- Added @onready refs, tab handler for index 6
- `_load_chat_config()` — fetches and populates UI
- `_on_wipe_chat()` — confirmation dialog → delegates to lobby's `admin_wipe_chat()`
- `_on_purge_old_chat()` — confirmation dialog → delegates to lobby's `admin_purge_chat()`
- `_on_save_chat_config()` — reads UI → saves to server

### `scenes/lobby.gd`
- `admin_wipe_chat()` — calls `BackendService.admin_clear_global_chat`, clears local messages
- `admin_purge_chat(max_age_days)` — calls `BackendService.admin_purge_old_messages`, returns count

### `scenes/ui/lobby_chat.gd`
- Added `_chat_config` dictionary
- `join_global_chat()` now fetches admin config, uses `max_messages` for history limit, injects prefix system message at top of chat

## Config storage
- Collection: `config` / Key: `lobby_chat` / User: system user
- Shape: `{ "prefix": "", "max_messages": 50, "max_age_days": 0 }`
