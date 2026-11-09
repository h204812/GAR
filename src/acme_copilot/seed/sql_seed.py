from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_SQL = """\
-- Acme Knowledge Copilot — relational schema (Phase 0A)
-- Load into Postgres in Phase 0B.

CREATE TABLE IF NOT EXISTS teams (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    slack_channel TEXT,
    oncall_rotation TEXT
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    team_id TEXT NOT NULL REFERENCES teams(id),
    role TEXT NOT NULL,
    level TEXT,
    hire_date DATE,
    manager_id INTEGER REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS slas (
    team_id TEXT NOT NULL REFERENCES teams(id),
    severity TEXT NOT NULL,
    response_minutes INTEGER NOT NULL,
    resolve_hours INTEGER NOT NULL,
    PRIMARY KEY (team_id, severity)
);

CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    owner_team_id TEXT NOT NULL REFERENCES teams(id),
    environment TEXT NOT NULL,
    service_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS incidents (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    severity TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    mitigated_at TIMESTAMPTZ,
    primary_service TEXT NOT NULL,
    owner_team TEXT NOT NULL REFERENCES teams(id)
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    team_id TEXT NOT NULL REFERENCES teams(id),
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    resolved_at TIMESTAMPTZ,
    assignee_id INTEGER REFERENCES employees(id),
    service TEXT
);

CREATE TABLE IF NOT EXISTS incident_tickets (
    incident_id TEXT NOT NULL REFERENCES incidents(id),
    ticket_id INTEGER NOT NULL REFERENCES tickets(id),
    PRIMARY KEY (incident_id, ticket_id)
);
"""


def _sql_str(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace("'", "''")
    return f"'{text}'"


def generate_sql(
    manifest: dict[str, Any],
    employees: list[dict[str, Any]],
    tickets: list[dict[str, Any]],
    out_dir: Path,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "schema.sql").write_text(SCHEMA_SQL, encoding="utf-8")

    lines: list[str] = ["BEGIN;", ""]

    for team in manifest["teams"]:
        lines.append(
            "INSERT INTO teams (id, name, slack_channel, oncall_rotation) VALUES ("
            f"{_sql_str(team['id'])}, {_sql_str(team['name'])}, "
            f"{_sql_str(team['slack_channel'])}, {_sql_str(team.get('oncall_rotation'))});"
        )

    lines.append("")
    # Insert employees without manager_id first, then update — avoid FK order issues
    for e in employees:
        lines.append(
            "INSERT INTO employees (id, name, email, team_id, role, level, hire_date, manager_id) VALUES ("
            f"{e['id']}, {_sql_str(e['name'])}, {_sql_str(e['email'])}, {_sql_str(e['team_id'])}, "
            f"{_sql_str(e['role'])}, {_sql_str(e['level'])}, {_sql_str(e['hire_date'])}, NULL);"
        )
    for e in employees:
        if e["manager_id"] is not None:
            lines.append(
                f"UPDATE employees SET manager_id = {e['manager_id']} WHERE id = {e['id']};"
            )

    lines.append("")
    for team in manifest["teams"]:
        for sla in manifest["slas"]:
            lines.append(
                "INSERT INTO slas (team_id, severity, response_minutes, resolve_hours) VALUES ("
                f"{_sql_str(team['id'])}, {_sql_str(sla['severity'])}, "
                f"{sla['response_minutes']}, {sla['resolve_hours']});"
            )

    lines.append("")
    asset_id = 1
    for svc in manifest["services"]:
        for env in ("prod", "staging"):
            kind = "datastore" if svc.get("kind") == "datastore" else "service"
            lines.append(
                "INSERT INTO assets (id, type, owner_team_id, environment, service_name) VALUES ("
                f"{asset_id}, {_sql_str(kind)}, {_sql_str(svc['owner_team'])}, "
                f"{_sql_str(env)}, {_sql_str(svc['name'])});"
            )
            asset_id += 1

    lines.append("")
    for inc in manifest["incidents"]:
        lines.append(
            "INSERT INTO incidents (id, title, severity, started_at, mitigated_at, primary_service, owner_team) VALUES ("
            f"{_sql_str(inc['id'])}, {_sql_str(inc['title'])}, {_sql_str(inc['severity'])}, "
            f"{_sql_str(inc['started_at'])}, {_sql_str(inc['mitigated_at'])}, "
            f"{_sql_str(inc['primary_service'])}, {_sql_str(inc['owner_team'])});"
        )

    lines.append("")
    for t in tickets:
        lines.append(
            "INSERT INTO tickets (id, title, team_id, severity, status, created_at, resolved_at, assignee_id, service) VALUES ("
            f"{t['id']}, {_sql_str(t['title'])}, {_sql_str(t['team_id'])}, {_sql_str(t['severity'])}, "
            f"{_sql_str(t['status'])}, {_sql_str(t['created_at'])}, {_sql_str(t['resolved_at'])}, "
            f"{t['assignee_id']}, {_sql_str(t['service'])});"
        )

    # Link a few tickets to incidents by service + time window (simple heuristic)
    lines.append("")
    for inc in manifest["incidents"]:
        linked = 0
        for t in tickets:
            if t["service"] == inc["primary_service"] and linked < 3:
                lines.append(
                    "INSERT INTO incident_tickets (incident_id, ticket_id) VALUES ("
                    f"{_sql_str(inc['id'])}, {t['id']});"
                )
                linked += 1

    lines.extend(["", "COMMIT;", ""])
    (out_dir / "seed.sql").write_text("\n".join(lines), encoding="utf-8")

    # JSON snapshots for inspection / SQLite loaders later
    snapshot = {
        "teams": manifest["teams"],
        "employees": employees,
        "tickets": tickets,
        "incidents": manifest["incidents"],
        "slas": manifest["slas"],
        "services": manifest["services"],
    }
    (out_dir / "snapshot.json").write_text(
        json.dumps(snapshot, indent=2) + "\n", encoding="utf-8"
    )
