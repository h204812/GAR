---
doc_id: postmortem-inc-2024-1201
doc_type: postmortem
incident_id: INC-2024-1201
service: inventory-api
team: inventory
last_updated: 2024-12-01
source: synthetic
title: "Postmortem: Inventory stock mismatch during flash sale"
---

# Postmortem: INC-2024-1201 — Inventory stock mismatch during flash sale

## Summary

Cache TTL misconfiguration returned stale stock counts.

## Timeline

- Started: `2024-12-01T18:00:00Z`
- Mitigated: `2024-12-01T20:30:00Z`
- Severity: **Sev-2**
- Primary service: `inventory-api`
- Related: catalog-api

## Impact

Customer-facing errors and elevated latency on dependent services.

## Root cause

See summary. Action items tracked in tickets linked to `INC-2024-1201`.

## Action items

1. Add connection-pool alerts for related datastores.
2. Update the `inventory-api-runbook` with this failure mode.
3. Schedule a game day for the owning team (**inventory**).
