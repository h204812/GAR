from __future__ import annotations

import itertools
from typing import Any


def build_employees(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Deterministic ~80 employees across teams from name lists + roles."""
    first = manifest["employee_first_names"]
    last = manifest["employee_last_names"]
    teams = manifest["teams"]
    roles_by_team = manifest["roles_by_team"]

    name_cycle = itertools.cycle(
        f"{f} {l}" for f, l in itertools.product(first, last)
    )
    employees: list[dict[str, Any]] = []
    emp_id = 1

    # ~6–8 people per eng team, fewer for ops
    target_per_team = {
        "hr": 4,
        "finance": 4,
        "support": 5,
    }

    for team in teams:
        tid = team["id"]
        n = target_per_team.get(tid, 7)
        roles = roles_by_team[tid]
        for i in range(n):
            name = next(name_cycle)
            slug = name.lower().replace(" ", ".")
            role = roles[i % len(roles)]
            level = "L5" if "Staff" in role or "Manager" in role else "L3" if i % 3 else "L4"
            employees.append(
                {
                    "id": emp_id,
                    "name": name,
                    "email": f"{slug}@{manifest['company']['domain']}",
                    "team_id": tid,
                    "role": role,
                    "level": level,
                    "hire_date": f"20{18 + (emp_id % 6)}-{(emp_id % 12) + 1:02d}-15",
                    "manager_id": None,
                }
            )
            emp_id += 1

    # Assign managers: first Engineering Manager (or first person) per team
    by_team: dict[str, list[dict[str, Any]]] = {}
    for e in employees:
        by_team.setdefault(e["team_id"], []).append(e)

    for tid, members in by_team.items():
        managers = [m for m in members if "Manager" in m["role"]]
        manager = managers[0] if managers else members[0]
        for m in members:
            if m["id"] != manager["id"]:
                m["manager_id"] = manager["id"]

    return employees
