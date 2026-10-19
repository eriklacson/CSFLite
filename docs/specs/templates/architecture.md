---
doc: architecture
mode: audit            # audit | design
system: UNSPECIFIED
version: 0.1
date: YYYY-MM-DD
source: UNSPECIFIED    # audit: <repo>@<commit>  |  design: <design-ref>
---

# Architecture — {{SYSTEM}}

> **Mode.** `audit` = this describes what was observed in source. `design` = this describes what is to be built.
> **Status vocabulary.** `CONFIRMED` · `PARTIAL` · `ABSENT` · `UNSPECIFIED` (audit: not determinable from source / design: not yet decided) · `UNVERIFIED` (claimed, not confirmed)
> **Evidence column.** audit = `file:line`. design = decision or requirement ID.
> **Named components only.** Every component carries its specific product name. Never a generic label, never a guess.

---

## 1. Purpose

One sentence. What the system does, for whom.

---

## 2. System context

Who uses it (actor types). What it talks to (external systems, named). What it is not responsible for.

---

## 3. Stack

| Layer | Component | Version | Status | Evidence |
|---|---|---|---|---|
| Language / runtime | | | | |
| Application framework | | | | |
| Data layer / ORM | | | | |
| Database | | | | |
| Auth | | | | |
| Hosting / deploy target | | | | |
| CI | | | | |

Add rows as needed. Do not delete rows — mark them `ABSENT` or `UNSPECIFIED`.

---

## 4. Runtime topology

Processes and runtimes in play. Where each runs. Note any split that changes available APIs or trust properties (e.g. two runtimes, server vs client execution, edge vs node).

| Runtime | What runs there | Trust properties | Status | Evidence |
|---|---|---|---|---|

---

## 5. Trust boundaries

The core section. Every point where trust changes.

| ID | Boundary | From → To | Enforcement mechanism | Enforcement location | Status | Evidence |
|---|---|---|---|---|---|---|
| TB-1 | Unauthenticated → authenticated | | | | | |
| TB-2 | Tenant A → tenant B | | | | | |
| TB-3 | User role → elevated action | | | | | |
| TB-4 | Application → external service | | | | | |

**Enforcement location** is the load-bearing field. Query layer, middleware, route handler, client, or none.

---

## 6. Data classes

What sensitive data exists and where it lives. No values, ever.

| Data class | Location (model / store) | Sensitivity | At-rest handling | Status | Evidence |
|---|---|---|---|---|---|

---

## 7. Decisions and rationale

| ID | Decision | Rationale | Status | Evidence |
|---|---|---|---|---|
| AD-1 | | | | |

**audit mode:** usually empty or `ABSENT`. That absence is the provenance finding — record it, do not manufacture rationale.
**design mode:** this section is the contract. A coding agent reads it before changing anything above.

---

## 8. Open items

| ID | Item | Why unresolved | Owner | Blocks |
|---|---|---|---|---|

`UNSPECIFIED` and `UNVERIFIED` entries from any section above are carried here.
