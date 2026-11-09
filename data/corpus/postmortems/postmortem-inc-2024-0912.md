---
doc_id: postmortem-inc-2024-0912
doc_type: postmortem
incident_id: INC-2024-0912
service: checkout-api
team: checkout
last_updated: 2024-09-12
source: synthetic
title: "Postmortem: Checkout checkout latency and payment failures"
---

# Postmortem: INC-2024-0912 — Checkout checkout latency and payment failures

## Summary

Downstream payments-ledger connection pool exhaustion caused checkout timeouts.

## Timeline

- Started: `2024-09-12T14:05:00Z`
- Mitigated: `2024-09-12T16:40:00Z`
- Severity: **Sev-1**
- Primary service: `checkout-api`
- Related: payments-ledger, auth-service

## Impact

Customer-facing errors and elevated latency on dependent services.

## Root cause

See summary. Action items tracked in tickets linked to `INC-2024-0912`.

## Action items

1. Add connection-pool alerts for related datastores.
2. Update the `checkout-api-runbook` with this failure mode.
3. Schedule a game day for the owning team (**checkout**).
