---
doc_id: payments-ledger-runbook
doc_type: runbook
service: payments-ledger
team: payments
severity: Sev-1
last_updated: 2024-11-10
source: synthetic
title: payments-ledger On-call Runbook
---

# payments-ledger — On-call Runbook

## Ownership

- Owning team: **payments**
- Tier: **0**
- Repo: `github.com/acme/payments-ledger`

## Symptoms

- Elevated 5xx or latency on `payments-ledger`
- Downstream dependency errors: auth-service, payments-db

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `payments-ledger`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback payments-ledger --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
