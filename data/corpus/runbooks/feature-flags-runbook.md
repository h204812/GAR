---
doc_id: feature-flags-runbook
doc_type: runbook
service: feature-flags
team: platform
severity: Sev-2
last_updated: 2024-08-01
source: synthetic
title: feature-flags On-call Runbook
---

# feature-flags — On-call Runbook

## Ownership

- Owning team: **platform**
- Tier: **2**
- Repo: `github.com/acme/feature-flags`

## Symptoms

- Elevated 5xx or latency on `feature-flags`
- Downstream dependency errors: redis-flags

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `feature-flags`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback feature-flags --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
