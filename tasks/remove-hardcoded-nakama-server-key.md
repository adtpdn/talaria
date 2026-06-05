---
title: "Remove Hardcoded Nakama Server Key"
id: "004"
status: done
priority: 01
sprint: alpha
category: SECURITY
description: "nakama_manager.gd contains hardcoded server key 'defaultkey' which is a critical security vulnerability. Server keys should never be in client code."
---
## Problem

File: scripts/nakama_manager.gd line 4

```javascript
var nakama_server_key = "defaultkey"
```

The Nakama server key is hardcoded in client code, which is a critical security vulnerability. Anyone can decompile the game and extract this key to make unauthorized API calls.

## Solution

1. Remove the hardcoded key from nakama_manager.gd
1. Configure the server key in Nakama server configuration only
1. Use Nakama's public API endpoints that don't require server keys for client authentication
1. If server key is needed for specific operations, move those to server-side RPC functions
## Acceptance Criteria

- [ ] Server key removed from client code
- [ ] Client authentication works without hardcoded key
- [ ] No server keys found in any client-side scripts
- [ ] Verified in exported builds (decompile check)
## References

- Nakama Security Best Practices: https://heroiclabs.com/docs/nakama/concepts/authentication/
- Knowledge Base: Auth & Secrets Lockdown
