---
doc_id: billing-api-runbook
doc_type: runbook
service: billing-api
team: finance
severity: Sev-2
last_updated: 2024-08-01
source: synthetic
title: billing-api On-call Runbook
---

# billing-api — On-call Runbook

## Ownership

- Owning team: **finance**
- Tier: **1**
- Repo: `github.com/acme/billing-api`

## Symptoms

- Elevated 5xx or latency on `billing-api`
- Downstream dependency errors: payments-ledger

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `billing-api`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback billing-api --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
