---
doc_id: notification-svc-runbook
doc_type: runbook
service: notification-svc
team: notifications
severity: Sev-2
last_updated: 2024-08-01
source: synthetic
title: notification-svc On-call Runbook
---

# notification-svc — On-call Runbook

## Ownership

- Owning team: **notifications**
- Tier: **1**
- Repo: `github.com/acme/notification-svc`

## Symptoms

- Elevated 5xx or latency on `notification-svc`
- Downstream dependency errors: redis-notif

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `notification-svc`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback notification-svc --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
