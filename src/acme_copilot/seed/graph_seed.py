from __future__ import annotations

from pathlib import Path
from typing import Any


def _esc(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def generate_graph(
    manifest: dict[str, Any],
    employees: list[dict[str, Any]],
    out_dir: Path,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "// Acme Knowledge Copilot — Neo4j seed (Phase 0A)",
        "// Apply with cypher-shell or Neo4j Browser in Phase 0B.",
        "",
        "MATCH (n) DETACH DELETE n;",
        "",
        "CREATE CONSTRAINT team_id IF NOT EXISTS FOR (t:Team) REQUIRE t.id IS UNIQUE;",
        "CREATE CONSTRAINT service_name IF NOT EXISTS FOR (s:Service) REQUIRE s.name IS UNIQUE;",
        "CREATE CONSTRAINT person_email IF NOT EXISTS FOR (p:Person) REQUIRE p.email IS UNIQUE;",
        "CREATE CONSTRAINT incident_id IF NOT EXISTS FOR (i:Incident) REQUIRE i.id IS UNIQUE;",
        "",
    ]

    for team in manifest["teams"]:
        lines.append(
            f"CREATE (:Team {{id: '{_esc(team['id'])}', name: '{_esc(team['name'])}', "
            f"slack: '{_esc(team['slack_channel'])}'}});"
        )

    lines.append("")
    for svc in manifest["services"]:
        kind = svc.get("kind", "service")
        label = "Datastore" if kind == "datastore" else "Service"
        repo = svc.get("repo") or ""
        lines.append(
            f"CREATE (:{label} {{name: '{_esc(svc['name'])}', tier: {svc['tier']}, "
            f"repo: '{_esc(repo)}', kind: '{_esc(kind)}'}});"
        )

    lines.append("")
    for e in employees:
        lines.append(
            f"CREATE (:Person {{id: {e['id']}, name: '{_esc(e['name'])}', "
            f"email: '{_esc(e['email'])}', role: '{_esc(e['role'])}'}});"
        )

    lines.append("")
    for inc in manifest["incidents"]:
        lines.append(
            f"CREATE (:Incident {{id: '{_esc(inc['id'])}', title: '{_esc(inc['title'])}', "
            f"severity: '{_esc(inc['severity'])}', started_at: '{_esc(inc['started_at'])}'}});"
        )

    lines.append("")
    # Relationships
    for svc in manifest["services"]:
        label = "Datastore" if svc.get("kind") == "datastore" else "Service"
        lines.append(
            f"MATCH (s:{label} {{name: '{_esc(svc['name'])}'}}), "
            f"(t:Team {{id: '{_esc(svc['owner_team'])}'}}) "
            f"CREATE (s)-[:OWNED_BY]->(t);"
        )
        for dep in svc.get("depends_on") or []:
            # dep may be Service or Datastore
            lines.append(
                f"MATCH (a {{name: '{_esc(svc['name'])}'}}), (b {{name: '{_esc(dep)}'}}) "
                f"CREATE (a)-[:DEPENDS_ON]->(b);"
            )

    lines.append("")
    for e in employees:
        lines.append(
            f"MATCH (p:Person {{email: '{_esc(e['email'])}'}}), "
            f"(t:Team {{id: '{_esc(e['team_id'])}'}}) "
            f"CREATE (p)-[:MEMBER_OF]->(t);"
        )

    lines.append("")
    for team in manifest["teams"]:
        if not team.get("oncall_rotation"):
            continue
        # Team responds to services it owns
        for svc in manifest["services"]:
            if svc["owner_team"] == team["id"] and svc.get("kind") != "datastore":
                lines.append(
                    f"MATCH (t:Team {{id: '{_esc(team['id'])}'}}), "
                    f"(s:Service {{name: '{_esc(svc['name'])}'}}) "
                    f"CREATE (t)-[:RESPONDS_TO]->(s);"
                )

    lines.append("")
    for inc in manifest["incidents"]:
        lines.append(
            f"MATCH (i:Incident {{id: '{_esc(inc['id'])}'}}), "
            f"(s:Service {{name: '{_esc(inc['primary_service'])}'}}) "
            f"CREATE (i)-[:AFFECTED]->(s);"
        )
        for rel in inc.get("related_services") or []:
            lines.append(
                f"MATCH (i:Incident {{id: '{_esc(inc['id'])}'}}), (s {{name: '{_esc(rel)}'}}) "
                f"CREATE (i)-[:AFFECTED]->(s);"
            )

    lines.append("")
    (out_dir / "seed.cypher").write_text("\n".join(lines), encoding="utf-8")
