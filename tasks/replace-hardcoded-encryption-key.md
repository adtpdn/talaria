---
title: "Replace Hardcoded Encryption Key"
id: "005"
status: done
priority: 01
sprint: alpha
category: SECURITY
description: "auth_manager.gd uses weak hardcoded encryption key 'tekton_secret_key_change_me_123' for session storage. Needs cryptographically secure key generation."
---
## Problem

File: scripts/managers/auth_manager.gd line 21

```javascript
const ENCRYPTION_KEY := "tekton_secret_key_change_me_123"
```

The encryption key for session storage:

1. Is hardcoded (comment says "change_me" but never changed)
1. Is weak and predictable
1. Is the same for all users
1. Can be extracted from decompiled builds
## Solution

1. Generate a unique encryption key per device using OS.get_unique_id() + secure random salt
1. Store the generated key in OS keychain/keystore (platform-specific)
1. For desktop, use Godot's encrypted file storage with device-specific key
1. Implement key rotation mechanism
## Implementation

```javascript
func _get_encryption_key() -> String:
    var key_file := "user://encryption_key.dat"
    if FileAccess.file_exists(key_file):
        var f := FileAccess.open(key_file, FileAccess.READ)
        return f.get_as_text()
    
    # Generate new key
    var device_id := OS.get_unique_id()
    var random_salt := str(randi()) + str(Time.get_ticks_msec())
    var key := (device_id + random_salt).sha256_text()
    
    var f := FileAccess.open(key_file, FileAccess.WRITE)
    f.store_string(key)
    return key
```

## Acceptance Criteria

- [ ] Unique encryption key per device
- [ ] Key not hardcoded in source
- [ ] Session encryption/decryption works
- [ ] Key persists across app restarts
- [ ] Tested on all platforms (PC, Android, iOS)
