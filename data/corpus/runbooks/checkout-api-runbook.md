---
doc_id: checkout-api-runbook
doc_type: runbook
service: checkout-api
team: checkout
severity: Sev-1
last_updated: 2024-09-15
source: synthetic
title: checkout-api On-call Runbook
---

# checkout-api — On-call Runbook

## Ownership

- Owning team: **checkout**
- Tier: **0**
- Repo: `github.com/acme/checkout-api`

## Symptoms

- Elevated 5xx or latency on `checkout-api`
- Downstream dependency errors: payments-ledger, auth-service, inventory-api, notification-svc

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `checkout-api`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback checkout-api --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
