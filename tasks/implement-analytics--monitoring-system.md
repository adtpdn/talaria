---
title: "Implement Analytics & Monitoring System"
id: "013"
status: todo
priority: 02
sprint: alpha
category: ANALYTICS
description: "Build a comprehensive telemetry system for tracking player behavior, crashes, performance, and business metrics (DAU, Retention, ARPU)."
---

# Implement Analytics & Monitoring System

## Problem
The project operates "blind" in production. Without a system to track player behavior, monitor performance, or report crashes, it is impossible to measure success (DAU, retention), identify friction in the tutorial, debug production crashes, or optimize performance across different hardware.

## Solution
Implement a multi-layered monitoring architecture consisting of a client-side `AnalyticsService`, server-side aggregation, and a crash reporting utility.

### Implementation Details
1. **Client-Side `AnalyticsService`:**
    - Define an `EventType` enum (SESSION_START, GACHA_PULL, etc.).
    - Implement `track_event(event, properties)` that handles session IDs, timestamps, and platform metadata via `rpc_async("track_analytics_event", ...)`.
2. **Server-Side Aggregation:**
    - Implement a Nakama Lua module to store raw events in an `analytics` collection.
    - Create a `daily_metrics` system to track DAU and revenue in real-time.
3. **Crash Reporting:**
    - Create `crash_reporter.gd` to hook into Godot's crash notifications, save dumps locally (`user://`), and upload them to the server.
4. **Performance Monitoring:**
    - Implement `performance_monitor.gd` to sample FPS and frame times, reporting averages every 60 frames.

## Benefits
- **Data-Driven Decisions:** Allows iteration on gameplay based on actual player behavior.
- **Proactive Bug Fixing:** Crash reports provide stack traces and device info, reducing time-to-fix.
- **Business Visibility:** Immediate insight into monetization (ARPU) and user growth (DAU).

## Acceptance Criteria
- **Telemetry Accuracy:** Verify `track_event` sends data to Nakama with valid `session_id` and `user_id`.
- **Crash Reporting Flow:** Trigger a forced crash and verify that a `.json` report is created in `user://` and sent to the server.
- **Performance Metrics:** Verify FPS and frame time metrics are reported without impacting game performance.
- **Server Aggregation:** Verify `daily_metrics` collection increments DAU on `SESSION_START`.
- **Privacy Compliance:** Implement and verify a user "Opt-out of Analytics" toggle in Settings.

## Migration Checklist
- [ ] Implement `scripts/services/analytics_service.gd` with the `EventType` enum.
- [ ] Implement `scripts/utils/crash_reporter.gd` and hook it into the main scene.
- [ ] Implement `scripts/utils/performance_monitor.gd` as an autoload.
- [ ] Deploy the `analytics.ts` Lua module to the Nakama server.
- [ ] Create the `daily_metrics` storage logic in the backend.
- [ ] Integrate the analytics opt-out toggle into the Settings UI.
- [ ] Verify telemetry data via SQL query against the Nakama collection.
