---
title: "Implement Regional Server Infrastructure"
id: "009"
status: todo
priority: 01
sprint: alpha
category: BACKEND
description: "Deploy multi-region server clusters (EU, China/HK, APAC) to ensure low latency, GFW-aware routing, and regional regulatory compliance (GDPR)."
---

# Implement Regional Server Infrastructure

## Problem
The project currently relies on a single hardcoded server, creating three critical risks:
1. **High Latency:** Severe lag for APAC players connecting to EU servers.
2. **Regulatory Non-Compliance:** GDPR and other regional laws require specific data handling for residents.
3. **Connectivity Issues:** The Great Firewall (GFW) often throttles generic VPS providers, making the game unstable in China.

## Solution
Deploy a distributed server architecture with regional clusters and an automated routing system.

### Deployment Architecture
1. **Regional Clusters:** 
    - **EU West:** Nakama on Webdock.io (Frankfurt/Amsterdam) with CockroachDB for GDPR compliance.
    - **Asia East:** Gateway on HostHatch.com (Hong Kong) for GFW-aware routing.
    - **APAC Edge:** Nodes in Tokyo, Seoul, and Singapore.
2. **Automated Region Manager:** Implement a `RegionManager` singleton detecting region via `OS.get_locale()` and `Time.get_time_zone_from_system()`, then performing a latency-based "ping" test.
3. **Geo-DNS Integration:** Use Geo-DNS (e.g., Cloudflare) to resolve `api.tektondash.com` to the nearest regional cluster.
4. **Compliance Routing:** Ensure EU resident data is routed exclusively to EU clusters.

## Benefits
- **Global Performance:** Minimal ping for all target markets, ensuring smooth sync.
- **Legal Safety:** Full compliance with GDPR, PIPA, and APPI.
- **Market Accessibility:** Reliable connectivity for players in China and restrictive environments.

## Acceptance Criteria
- **Region Detection:** Verify a user in Germany is routed to `EU_WEST` and a user in China to `ASIA_EAST`.
- **Latency Optimization:** Confirm the latency-based selection chooses the fastest endpoint.
- **Connectivity Verification:** Confirm game accessibility from within China via the HK gateway.
- **Compliance Validation:** Verify EU user data is stored exclusively in the EU CockroachDB cluster.
- **Manual Override:** Verify users can manually switch regions in Settings and reconnect.

## Migration Checklist
- [ ] Provision VPS instances on Webdock.io (EU) and HostHatch.com (HK).
- [ ] Deploy Nakama clusters to each regional VPS.
- [ ] Setup CockroachDB for cross-region synchronization and partitioning.
- [ ] Implement `scripts/services/region_manager.gd` for detection and routing.
- [ ] Configure Geo-DNS records for regional endpoints.
- [ ] Test connectivity and latency from EU, China, and Japan IPs.
- [ ] Audit data flows for GDPR compliance.
