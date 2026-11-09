---
doc_id: inventory-api-runbook
doc_type: runbook
service: inventory-api
team: inventory
severity: Sev-2
last_updated: 2024-08-01
source: synthetic
title: inventory-api On-call Runbook
---

# inventory-api — On-call Runbook

## Ownership

- Owning team: **inventory**
- Tier: **1**
- Repo: `github.com/acme/inventory-api`

## Symptoms

- Elevated 5xx or latency on `inventory-api`
- Downstream dependency errors: inventory-db

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `inventory-api`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback inventory-api --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
