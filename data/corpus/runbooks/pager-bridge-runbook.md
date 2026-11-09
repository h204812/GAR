---
doc_id: pager-bridge-runbook
doc_type: runbook
service: pager-bridge
team: sre
severity: Sev-2
last_updated: 2024-08-01
source: synthetic
title: pager-bridge On-call Runbook
---

# pager-bridge — On-call Runbook

## Ownership

- Owning team: **sre**
- Tier: **1**
- Repo: `github.com/acme/pager-bridge`

## Symptoms

- Elevated 5xx or latency on `pager-bridge`
- Downstream dependency errors: notification-svc

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `pager-bridge`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback pager-bridge --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
