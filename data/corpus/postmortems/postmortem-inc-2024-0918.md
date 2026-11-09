---
doc_id: postmortem-inc-2024-0918
doc_type: postmortem
incident_id: INC-2024-0918
service: auth-service
team: identity
last_updated: 2024-09-18
source: synthetic
title: "Postmortem: Auth session stampede after redis failover"
---

# Postmortem: INC-2024-0918 — Auth session stampede after redis failover

## Summary

Redis failover without warm replicas caused session lookup spikes.

## Timeline

- Started: `2024-09-18T09:20:00Z`
- Mitigated: `2024-09-18T11:05:00Z`
- Severity: **Sev-2**
- Primary service: `auth-service`
- Related: redis-sessions

## Impact

Customer-facing errors and elevated latency on dependent services.

## Root cause

See summary. Action items tracked in tickets linked to `INC-2024-0918`.

## Action items

1. Add connection-pool alerts for related datastores.
2. Update the `auth-service-runbook` with this failure mode.
3. Schedule a game day for the owning team (**identity**).
