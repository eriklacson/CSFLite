---
doc: routes
mode: audit            # audit | design
system: UNSPECIFIED
version: 0.1
date: YYYY-MM-DD
source: UNSPECIFIED    # audit: <repo>@<commit>  |  design: <design-ref>
---

# Routes — {{SYSTEM}}

> **Mode.** `audit` = routes observed in source. `design` = routes to be built.
> **Status vocabulary.** `CONFIRMED` · `PARTIAL` · `ABSENT` · `UNSPECIFIED` · `UNVERIFIED`
> **Evidence column.** audit = `file:line`. design = requirement ID.
> **Record, do not judge.** In audit mode this is an inventory. Candidate findings are parked, not expanded here.

---

## 1. Inventory

One row per route. Group by area. Add a `### <area>` heading per group.

| ID | Method | Path | Handler | Auth required | Tenant-scoped | Input source | Sink | Status | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| R-1 | | | | | | | | | |

**Column vocabulary**

- **Auth required** — `yes` / `no` / `UNSPECIFIED`. In audit mode this is what the code does, not what it should do.
- **Tenant-scoped** — `yes` / `no` / `n/a` (route touches no tenant data) / `UNSPECIFIED`.
- **Input source** — `body` / `query` / `params` / `header` / `none`. Multiple allowed.
- **Sink** — where input lands: `query` / `external-api` / `file-path` / `command` / `redirect` / `render` / `none`.

The last two columns pre-feed the input-validation check. The two before them pre-feed the boundary trace.

---

## 2. Unauthenticated surface

Every route from §1 where **Auth required** is `no` or `UNSPECIFIED`. Restate them here — this list is read on its own.

| ID | Method | Path | Intentional? | Evidence |
|---|---|---|---|---|

**Intentional?** — audit: `UNSPECIFIED` unless a decision record says otherwise. design: `yes` with an AD- reference, or the route does not ship.

---

## 3. Elevated-permission surface

Routes requiring a role, permission, or admin guard.

| ID | Method | Path | Guard | Checked server-side? | Status | Evidence |
|---|---|---|---|---|---|---|

---

## 4. Middleware and route-level interceptors

| ID | Name | Applies to (path pattern) | Responsibility | Status | Evidence |
|---|---|---|---|---|---|

Note anything that matches by pattern — a path that falls outside the pattern is an unprotected route even when §1 shows a guard.

---

## 5. Coverage

| Measure | Count |
|---|---|
| Total routes | |
| Auth required: yes | |
| Auth required: no | |
| Auth: UNSPECIFIED | |
| Tenant-scoped: yes | |
| Tenant-scoped: no, touching tenant data | |

Counts only. No severity, no verdict.

---

## 6. Open items

| ID | Item | Why unresolved | Blocks |
|---|---|---|---|
