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
