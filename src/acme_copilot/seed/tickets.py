from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from typing import Any


SEVERITIES = ["Sev-1", "Sev-2", "Sev-3", "Sev-4"]
STATUSES = ["open", "in_progress", "resolved", "closed"]

TITLES = [
    "Elevated error rate on {service}",
    "Latency spike: {service}",
    "Deploy rollback for {service}",
    "Capacity warning: {service}",
    "Customer report: {service} timeouts",
    "Alert: {service} dependency unhealthy",
    "Runbook gap for {service}",
    "On-call page: {service}",
]


def build_tickets(
    manifest: dict[str, Any],
    employees: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rng = random.Random(manifest["seed"])
    total = manifest["ticket_counts"]["total"]
    payments_sev1_q3 = manifest["ticket_counts"]["payments_sev1_q3_2024"]

    eng_teams = [
        t["id"]
        for t in manifest["teams"]
        if t["id"] not in {"hr", "finance"}
    ]
    services = [
        s["name"]
        for s in manifest["services"]
        if s.get("kind") != "datastore"
    ]
    by_team = {t: [e for e in employees if e["team_id"] == t] for t in eng_teams}

    tickets: list[dict[str, Any]] = []
    ticket_id = 1

    # Guaranteed gold: Payments Sev-1 in Q3 2024 (Jul 1 – Sep 30)
    q3_start = datetime(2024, 7, 1, tzinfo=timezone.utc)
    for i in range(payments_sev1_q3):
        created = q3_start + timedelta(days=10 * i + 3, hours=8 + i)
        assignee = by_team["payments"][i % len(by_team["payments"])]
        tickets.append(
            _ticket(
                ticket_id,
                team_id="payments",
                severity="Sev-1",
                status="resolved",
                created=created,
                service="payments-ledger",
                assignee_id=assignee["id"],
                rng=rng,
            )
        )
        ticket_id += 1

    # Remaining tickets scattered 2024-01 .. 2024-12
    year_start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    while len(tickets) < total:
        team_id = rng.choice(eng_teams)
        severity = rng.choices(SEVERITIES, weights=[5, 15, 40, 40], k=1)[0]
        # Avoid creating extra Payments Sev-1 in Q3
        created = year_start + timedelta(days=rng.randint(0, 364), hours=rng.randint(0, 23))
        if (
            team_id == "payments"
            and severity == "Sev-1"
            and datetime(2024, 7, 1, tzinfo=timezone.utc)
            <= created
            < datetime(2024, 10, 1, tzinfo=timezone.utc)
        ):
            severity = "Sev-2"

        service = rng.choice(services)
        members = by_team[team_id]
        assignee = rng.choice(members)
        status = rng.choices(STATUSES, weights=[10, 15, 40, 35], k=1)[0]
        tickets.append(
            _ticket(
                ticket_id,
                team_id=team_id,
                severity=severity,
                status=status,
                created=created,
                service=service,
                assignee_id=assignee["id"],
                rng=rng,
            )
        )
        ticket_id += 1

    tickets.sort(key=lambda t: t["created_at"])
    for i, t in enumerate(tickets, start=1):
        t["id"] = i
    return tickets


def _ticket(
    ticket_id: int,
    *,
    team_id: str,
    severity: str,
    status: str,
    created: datetime,
    service: str,
    assignee_id: int,
    rng: random.Random,
) -> dict[str, Any]:
    title_tmpl = rng.choice(TITLES)
    resolved_at = None
    if status in {"resolved", "closed"}:
        resolved_at = (created + timedelta(hours=rng.randint(1, 72))).isoformat().replace(
            "+00:00", "Z"
        )
    return {
        "id": ticket_id,
        "title": title_tmpl.format(service=service),
        "team_id": team_id,
        "severity": severity,
        "status": status,
        "created_at": created.isoformat().replace("+00:00", "Z"),
        "resolved_at": resolved_at,
        "assignee_id": assignee_id,
        "service": service,
    }
