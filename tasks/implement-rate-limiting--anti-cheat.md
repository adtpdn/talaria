---
title: "Implement Rate Limiting & Anti-Cheat"
id: "008"
status: todo
priority: 01
sprint: alpha
category: BACKEND
description: "Establish a multi-layer security system to prevent API abuse, memory editing, and botting through server-side rate limits and movement validation."
---

# Implement Rate Limiting & Anti-Cheat

## Problem
The application is vulnerable to common exploits:
1. **API Abuse:** Lack of rate limits allows attackers to flood the server with RPC calls, leading to DoS or database exhaustion.
2. **Economy Exploits:** Absence of server-side cooldowns on high-value actions (e.g., Gacha pulls) allows bot automation.
3. **Client-Side Manipulation:** Users can use memory editors (e.g., Cheat Engine) to modify wallet values or speed-hack.
4. **Botting:** Lack of behavioral analysis allows scripts to farm resources with inhuman timing.

## Solution
Implement a layered security architecture combining server-side authority with client-side friction.

### Security Layers
1. **Server-Side Rate Limiting:** 
    - Implement a `rate_limiter` module in Nakama.
    - Define `RATE_LIMITS` (e.g., `send_friend_request`: 10/min, `perform_gacha_pull`: 100/hr).
    - Wrap critical RPCs in a `rateLimitedRPC` handler tracking requests in storage.
2. **Client-Side Cooldowns:** Create a `CooldownManager` for immediate UI feedback and reduced server traffic.
3. **Movement Validation:** Implement a server-side `MultiplayerValidator` to check distance between positions against `max_speed * delta` and verify `pickup_range`.
4. **Integrity & Bot Detection:** 
    - Implement `integrity_checker.gd` using SHA-256 checksums of local data vs. server state.
    - Implement backend heuristics to flag accounts with unnaturally low variance in action timing.

## Benefits
- **Economic Stability:** Prevents hyper-inflation and exploitation of reward systems.
- **Fair Competition:** Ensures leaderboards and matches are won by skill, not hacks.
- **Infrastructure Protection:** Protects the Nakama server from malicious client loops.

## Acceptance Criteria
- **Rate Limit Enforcement:** Verify that exceeding 10 friend requests/min results in a "Rate limit exceeded" error.
- **Movement Validation:** Simulate a "speed hack" and verify the server detects the violation and corrects the player's position.
- **Integrity Checks:** Manually edit wallet value in memory and verify `integrity_checker.gd` forces a server sync.
- **Bot Detection:** Use a script to send requests with consistent 100ms intervals and verify account flagging.
- **UI Feedback:** Confirm `CooldownManager` correctly disables buttons and shows remaining time.

## Migration Checklist
- [ ] Implement `rate_limiter.ts` module in the Nakama server.
- [ ] Create `CooldownManager.gd` autoload singleton.
- [ ] Implement `MultiplayerValidator.gd` for movement and pickup checks.
- [ ] Build `integrity_checker.gd` with SHA-256 checksums.
- [ ] Integrate bot detection heuristics into backend session logic.
- [ ] Map and apply defined rate limits to all critical RPC functions.
- [ ] Implement an admin dashboard view to review and ban flagged accounts.
