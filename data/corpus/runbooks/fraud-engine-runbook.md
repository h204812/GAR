---
doc_id: fraud-engine-runbook
doc_type: runbook
service: fraud-engine
team: payments
severity: Sev-2
last_updated: 2024-08-01
source: synthetic
title: fraud-engine On-call Runbook
---

# fraud-engine — On-call Runbook

## Ownership

- Owning team: **payments**
- Tier: **1**
- Repo: `github.com/acme/fraud-engine`

## Symptoms

- Elevated 5xx or latency on `fraud-engine`
- Downstream dependency errors: payments-ledger

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `fraud-engine`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback fraud-engine --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
