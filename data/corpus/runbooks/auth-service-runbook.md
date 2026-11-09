---
doc_id: auth-service-runbook
doc_type: runbook
service: auth-service
team: identity
severity: Sev-1
last_updated: 2024-08-01
source: synthetic
title: auth-service On-call Runbook
---

# auth-service — On-call Runbook

## Ownership

- Owning team: **identity**
- Tier: **0**
- Repo: `github.com/acme/auth-service`

## Symptoms

- Elevated 5xx or latency on `auth-service`
- Downstream dependency errors: identity-db, redis-sessions

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `auth-service`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback auth-service --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
