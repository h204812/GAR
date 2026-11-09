---
doc_id: postmortem-inc-2024-1103
doc_type: postmortem
incident_id: INC-2024-1103
service: payments-ledger
team: payments
last_updated: 2024-11-04
source: synthetic
title: "Postmortem: Payments ledger write amplification"
---

# Postmortem: INC-2024-1103 — Payments ledger write amplification

## Summary

Incorrect retry loop on ledger writes overloaded payments-db.

## Timeline

- Started: `2024-11-03T21:10:00Z`
- Mitigated: `2024-11-04T01:25:00Z`
- Severity: **Sev-1**
- Primary service: `payments-ledger`
- Related: payments-db, fraud-engine

## Impact

Customer-facing errors and elevated latency on dependent services.

## Root cause

See summary. Action items tracked in tickets linked to `INC-2024-1103`.

## Action items

1. Add connection-pool alerts for related datastores.
2. Update the `payments-ledger-runbook` with this failure mode.
3. Schedule a game day for the owning team (**payments**).
