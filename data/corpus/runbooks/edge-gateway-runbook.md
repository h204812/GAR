---
doc_id: edge-gateway-runbook
doc_type: runbook
service: edge-gateway
team: platform
severity: Sev-1
last_updated: 2024-08-01
source: synthetic
title: edge-gateway On-call Runbook
---

# edge-gateway — On-call Runbook

## Ownership

- Owning team: **platform**
- Tier: **0**
- Repo: `github.com/acme/edge-gateway`

## Symptoms

- Elevated 5xx or latency on `edge-gateway`
- Downstream dependency errors: checkout-api, auth-service, catalog-api

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `edge-gateway`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback edge-gateway --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
