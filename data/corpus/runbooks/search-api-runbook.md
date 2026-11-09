---
doc_id: search-api-runbook
doc_type: runbook
service: search-api
team: platform
severity: Sev-2
last_updated: 2024-08-01
source: synthetic
title: search-api On-call Runbook
---

# search-api — On-call Runbook

## Ownership

- Owning team: **platform**
- Tier: **2**
- Repo: `github.com/acme/search-api`

## Symptoms

- Elevated 5xx or latency on `search-api`
- Downstream dependency errors: elasticsearch

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `search-api`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback search-api --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
