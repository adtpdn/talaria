---
title: "Remove Debug Code from Production"
id: "016"
status: todo
priority: 02
sprint: beta
category: CORE
description: "Debug code and test currency grants left in production. Need proper logging system and removal of test code from release builds."
---
## Problem

Debug code is left in production builds:

nakama_manager.gd line 102:

```javascript
if OS.is_debug_build():
    device_id += "_" + str(randi() % 1000)
```

player_movement_manager.gd line 502:

```javascript
print("[Debug] Checking Push Prevention for %s. Found %d stands." % [pos, stands.size()])
```

Multiple files:

- Debug print statements in hot paths
- Debug wireframe rendering code
- Test currency grants (gacha_panel.gd lines 85-87)
## Issues

- Performance impact from debug prints
- Confusing behavior differences between debug/release
- Test code accessible in production
- Debug UI elements visible to players
- Increased binary size
## Solution

### 1. Remove Test Code

gacha_panel.gd - Remove test currency grants:

```javascript
# DELETE THESE LINES:
UserProfileManager.wallet["star"] = 3200
UserProfileManager.wallet["gold"] = 1500
```

### 2. Proper Debug Logging System

```javascript
# scripts/utils/logger.gd (NEW FILE)
extends Node

enum LogLevel {
    DEBUG,
    INFO,
    WARNING,
    ERROR
}

var current_level: LogLevel = LogLevel.INFO
var log_to_file: bool = false
var log_file_path: String = "user://game.log"

func _ready() -> void:
    # Only enable debug logging in debug builds
    if OS.is_debug_build():
        current_level = LogLevel.DEBUG
        log_to_file = true

func debug(message: String, context: Dictionary = {}) -> void:
    if current_level <= LogLevel.DEBUG:
        _log("DEBUG", message, context)

func info(message: String, context: Dictionary = {}) -> void:
    if current_level <= LogLevel.INFO:
        _log("INFO", message, context)

func warning(message: String, context: Dictionary = {}) -> void:
    if current_level <= LogLevel.WARNING:
        _log("WARNING", message, context)

func error(message: String, context: Dictionary = {}) -> void:
    _log("ERROR", message, context)

func _log(level: String, message: String, context: Dictionary) -> void:
    var timestamp = Time.get_datetime_string_from_system()
    var log_line = "[%s] %s: %s" % [timestamp, level, message]
    
    if not context.is_empty():
        log_line += " | " + JSON.stringify(context)
    
    print(log_line)
    
    if log_to_file:
        _write_to_file(log_line)

func _write_to_file(line: String) -> void:
    var file = FileAccess.open(log_file_path, FileAccess.READ_WRITE)
    if file:
        file.seek_end()
        file.store_line(line)
        file.close()
```

### 3. Replace Debug Prints

Before:

```javascript
print("[Debug] Checking Push Prevention for %s. Found %d stands." % [pos, stands.size()])
```

After:

```javascript
Logger.debug("Checking Push Prevention", {"position": pos, "stands_count": stands.size()})
```

### 4. Feature Flags for Test Features

```javascript
# scripts/utils/feature_flags.gd (NEW FILE)
extends Node

const ENABLE_DEBUG_UI: bool = false  # Set via build config
const ENABLE_CHEAT_MENU: bool = false
const ENABLE_TEST_CURRENCY: bool = false

func is_feature_enabled(feature: String) -> bool:
    if not OS.is_debug_build():
        return false
    
    match feature:
        "debug_ui": return ENABLE_DEBUG_UI
        "cheat_menu": return ENABLE_CHEAT_MENU
        "test_currency": return ENABLE_TEST_CURRENCY
        _: return false
```

### 5. Export Configuration

export_presets.cfg:

```plain text
[preset.0.options]
script/encryption_key="your_encryption_key_here"
custom_template/debug=false
```

## Acceptance Criteria

- [ ] All test currency grants removed or feature-flagged
- [ ] Debug print statements replaced with Logger
- [ ] Logger only logs in debug builds
- [ ] No debug UI visible in release builds
- [ ] Debug wireframe code removed or feature-flagged
- [ ] Export presets configured correctly
- [ ] Verified in exported release build
- [ ] Performance profiling shows no debug overhead
## Files to Clean

- [ ] gacha_panel.gd (remove test currency)
- [ ] player_movement_manager.gd (replace debug prints)
- [ ] nakama_manager.gd (review debug device ID logic)
- [ ] skin_shader_generator.gd (feature-flag debug wireframe)
- [ ] All files with print("[Debug] statements
