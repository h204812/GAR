from __future__ import annotations

from pathlib import Path
from typing import Any


def _frontmatter(meta: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in meta.items():
        if value is None:
            continue
        if isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            # Quote strings that need it
            text = str(value)
            if any(c in text for c in ":#{}[]&*?|>!%@`"):
                lines.append(f'{key}: "{text}"')
            else:
                lines.append(f"{key}: {text}")
    lines.append("---")
    return "\n".join(lines)


def _write(path: Path, meta: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_frontmatter(meta) + "\n\n" + body.strip() + "\n", encoding="utf-8")


def generate_corpus(manifest: dict[str, Any], corpus_dir: Path) -> list[str]:
    """Write scripted markdown corpus. Returns list of doc_ids."""
    if corpus_dir.exists():
        for old in corpus_dir.rglob("*.md"):
            old.unlink()

    doc_ids: list[str] = []
    company = manifest["company"]["name"]
    policies = manifest["policies"]
    domain = manifest["company"]["domain"]

    # --- Policies ---
    docs: list[tuple[str, dict[str, Any], str]] = []

    docs.append(
        (
            "policies/pto-policy.md",
            {
                "doc_id": "pto-policy",
                "doc_type": "policy",
                "department": "hr",
                "last_updated": "2024-06-01",
                "source": "synthetic",
                "title": f"{company} PTO Policy",
            },
            f"""# {company} PTO Policy

## Eligibility

Full-time employees accrue paid time off based on role family.

## Engineer accrual

- Engineers receive **{policies['pto']['engineers_days_per_year']} days** of PTO per calendar year.
- Monthly accrual is **{policies['pto']['accrual_per_month']} days**.
- Maximum carryover into the next year is **{policies['pto']['carryover_max_days']} days**.
- Blackout months for engineering: {', '.join(policies['pto']['blackout_months'])}.

## Request process

Submit requests in Workday at least 5 business days in advance. Managers on `{domain}` must approve.
""",
        )
    )

    docs.append(
        (
            "policies/expense-policy.md",
            {
                "doc_id": "expense-policy",
                "doc_type": "policy",
                "department": "finance",
                "last_updated": "2024-05-15",
                "source": "synthetic",
                "title": f"{company} Expense Policy",
            },
            f"""# {company} Expense Policy

## Caps

- Meal cap: **USD {policies['expenses']['meal_cap_usd']}** per person per meal.
- Hotel cap: **USD {policies['expenses']['hotel_cap_usd']}** per night.
- Receipts required above **USD {policies['expenses']['requires_receipt_above_usd']}**.

## Foreign currency

{policies['expenses']['note']}

Submit expenses within 30 days via Concur.
""",
        )
    )

    docs.append(
        (
            "policies/remote-work-policy.md",
            {
                "doc_id": "remote-work-policy",
                "doc_type": "policy",
                "department": "hr",
                "last_updated": "2024-03-01",
                "source": "synthetic",
                "title": f"{company} Remote Work Policy",
            },
            f"""# {company} Remote Work Policy

Hybrid employees may work remotely up to **{policies['remote_work']['max_remote_days_per_week']} days** per week.

Core collaboration hours: **{policies['remote_work']['core_hours']}**.

Managers may require on-site presence for incident response weeks.
""",
        )
    )

    docs.append(
        (
            "policies/security-awareness.md",
            {
                "doc_id": "security-awareness",
                "doc_type": "policy",
                "department": "security",
                "classification": "internal",
                "last_updated": "2024-04-10",
                "source": "synthetic",
                "title": "Security Awareness Policy",
            },
            f"""# Security Awareness Policy

All employees complete phishing training within **{policies['security_awareness']['phishing_training_days']} days** of hire.

Laptop disk encryption is **{'required' if policies['security_awareness']['laptop_encryption_required'] else 'optional'}**.

Report suspicious mail to security@{domain}.
""",
        )
    )

    for name, title, body in [
        (
            "code-of-conduct",
            "Code of Conduct",
            "Treat colleagues with respect. Harassment is prohibited. Escalate to People Ops.",
        ),
        (
            "data-retention",
            "Data Retention Policy",
            "Customer PII is retained for 24 months after account closure unless legal hold applies.",
        ),
        (
            "vendor-access",
            "Vendor Access Policy",
            "Vendors require a ticket, time-bound SSO, and Security team approval before production access.",
        ),
        (
            "oncall-compensation",
            "On-call Compensation",
            "Primary on-call receives a weekly stipend. Incident commander overtime is tracked in Workday.",
        ),
    ]:
        docs.append(
            (
                f"policies/{name}.md",
                {
                    "doc_id": name,
                    "doc_type": "policy",
                    "department": "hr" if "conduct" in name or "oncall" in name else "security",
                    "last_updated": "2024-02-01",
                    "source": "synthetic",
                    "title": title,
                },
                f"# {title}\n\n{body}\n",
            )
        )

    # --- Wiki ---
    wiki_topics = [
        ("eng-onboarding", "Engineering Onboarding", "platform", "Complete laptop setup, SSO, and shadow an on-call shift in week two."),
        ("coding-standards", "Coding Standards", "platform", "Prefer typed Python/Go. All services need health checks and structured logs."),
        ("deploy-process", "Deploy Process", "platform", "Use canary deploys. Require two approvals for tier-0 services."),
        ("incident-command", "Incident Command", "sre", "IC owns communication. Use #incident-bridge. Page via pager-bridge."),
        ("observability", "Observability Guide", "sre", "RED metrics required. Traces for checkout and payments paths."),
        ("feature-flags-howto", "Feature Flags How-To", "platform", "Flags live in feature-flags service. Kill switches for payments flows."),
        ("sla-definitions", "SLA Definitions", "sre", "Sev-1 response is 15 minutes. Sev-1 resolve target is 4 hours."),
        ("local-dev-setup", "Local Dev Setup", "platform", "Use docker compose for datastores. Never point local tools at prod."),
        ("api-versioning", "API Versioning", "platform", "External APIs are versioned as /v1. Breaking changes need a deprecation window."),
        ("secrets-management", "Secrets Management", "security", "Store secrets in Vault. Rotate quarterly for tier-0 services."),
        ("capacity-planning", "Capacity Planning", "sre", "Flash sales require 2x inventory-api capacity and warm payments-db replicas."),
        ("customer-comms", "Customer Communications", "support", "Status page updates every 30 minutes during Sev-1 incidents."),
    ]
    for doc_id, title, team, blurb in wiki_topics:
        docs.append(
            (
                f"wiki/{doc_id}.md",
                {
                    "doc_id": doc_id,
                    "doc_type": "wiki",
                    "team": team,
                    "last_updated": "2024-07-01",
                    "source": "synthetic",
                    "title": title,
                },
                f"# {title}\n\n{blurb}\n\nOwned by the **{team}** team.\n",
            )
        )

    # --- Runbooks (one per major app service) ---
    app_services = [
        s
        for s in manifest["services"]
        if s.get("kind") != "datastore" and s["name"]
        in {
            "checkout-api",
            "payments-ledger",
            "auth-service",
            "inventory-api",
            "notification-svc",
            "order-orchestrator",
            "fraud-engine",
            "billing-api",
            "edge-gateway",
            "pager-bridge",
            "search-api",
            "feature-flags",
        }
    ]
    for svc in app_services:
        name = svc["name"]
        doc_id = f"{name}-runbook"
        updated = "2024-09-15" if name == "checkout-api" else "2024-08-01"
        if name == "payments-ledger":
            updated = "2024-11-10"
        docs.append(
            (
                f"runbooks/{doc_id}.md",
                {
                    "doc_id": doc_id,
                    "doc_type": "runbook",
                    "service": name,
                    "team": svc["owner_team"],
                    "severity": "Sev-1" if svc["tier"] == 0 else "Sev-2",
                    "last_updated": updated,
                    "source": "synthetic",
                    "title": f"{name} On-call Runbook",
                },
                f"""# {name} — On-call Runbook

## Ownership

- Owning team: **{svc['owner_team']}**
- Tier: **{svc['tier']}**
- Repo: `{svc.get('repo') or 'n/a'}`

## Symptoms

- Elevated 5xx or latency on `{name}`
- Downstream dependency errors: {', '.join(svc.get('depends_on') or ['none'])}

## Immediate actions

1. Acknowledge the page in PagerDuty.
2. Check dashboards for `{name}`.
3. If error budget burn is critical, start an incident channel.
4. Consider rollback of the last deploy.

## Rollback

```bash
acmectl rollback {name} --to previous
```

## Escalation

Page SRE if mitigation exceeds SLA response target.
""",
            )
        )

    # --- Postmortems tied to incidents ---
    for inc in manifest["incidents"]:
        doc_id = f"postmortem-{inc['id'].lower()}"
        docs.append(
            (
                f"postmortems/{doc_id}.md",
                {
                    "doc_id": doc_id,
                    "doc_type": "postmortem",
                    "incident_id": inc["id"],
                    "service": inc["primary_service"],
                    "team": inc["owner_team"],
                    "last_updated": inc["mitigated_at"][:10],
                    "source": "synthetic",
                    "title": f"Postmortem: {inc['title']}",
                },
                f"""# Postmortem: {inc['id']} — {inc['title']}

## Summary

{inc['summary']}

## Timeline

- Started: `{inc['started_at']}`
- Mitigated: `{inc['mitigated_at']}`
- Severity: **{inc['severity']}**
- Primary service: `{inc['primary_service']}`
- Related: {', '.join(inc['related_services'])}

## Impact

Customer-facing errors and elevated latency on dependent services.

## Root cause

See summary. Action items tracked in tickets linked to `{inc['id']}`.

## Action items

1. Add connection-pool alerts for related datastores.
2. Update the `{inc['primary_service']}-runbook` with this failure mode.
3. Schedule a game day for the owning team (**{inc['owner_team']}**).
""",
            )
        )

    # --- Architecture ---
    for svc in manifest["services"]:
        if svc.get("kind") == "datastore":
            continue
        if svc["name"] not in {
            "checkout-api",
            "payments-ledger",
            "auth-service",
            "inventory-api",
            "notification-svc",
            "order-orchestrator",
            "fraud-engine",
            "billing-api",
            "edge-gateway",
            "catalog-api",
        }:
            continue
        name = svc["name"]
        doc_id = f"{name}-architecture"
        deps = ", ".join(svc.get("depends_on") or ["none"])
        docs.append(
            (
                f"architecture/{doc_id}.md",
                {
                    "doc_id": doc_id,
                    "doc_type": "architecture",
                    "service": name,
                    "team": svc["owner_team"],
                    "last_updated": "2024-06-20",
                    "source": "synthetic",
                    "title": f"{name} Architecture",
                },
                f"""# {name} Architecture

## Overview

`{name}` is a tier-{svc['tier']} service owned by **{svc['owner_team']}**.

## Dependencies

{deps}

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
""",
            )
        )

    # --- Security docs ---
    security_docs = [
        ("pii-handling", "PII Handling", "Classify PII fields. Encrypt at rest. Access requires audit-log entries."),
        ("soc2-controls", "SOC2 Controls Overview", "Change management, access reviews, and incident response are in-scope controls."),
        ("access-reviews", "Access Reviews", "Quarterly access reviews for production roles. Managers attest in Workday."),
        ("vuln-management", "Vulnerability Management", "Critical CVEs on tier-0 services must be patched within 7 days."),
        ("secure-sdl", "Secure SDLC", "Threat models required for new tier-0 services before GA."),
        ("incident-security", "Security Incident Process", "Suspected breaches escalate to Security and Legal within 1 hour."),
    ]
    for doc_id, title, body in security_docs:
        docs.append(
            (
                f"security/{doc_id}.md",
                {
                    "doc_id": doc_id,
                    "doc_type": "policy",
                    "department": "security",
                    "classification": "internal",
                    "last_updated": "2024-05-01",
                    "source": "synthetic",
                    "title": title,
                },
                f"# {title}\n\n{body}\n",
            )
        )

    for rel_path, meta, body in docs:
        _write(corpus_dir / rel_path, meta, body)
        doc_ids.append(str(meta["doc_id"]))

    return doc_ids
