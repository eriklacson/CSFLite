---
doc: schema
mode: audit            # audit | design
system: UNSPECIFIED
tenant_field: UNSPECIFIED   # the tenant-scoping field name for this system
version: 0.1
date: YYYY-MM-DD
source: UNSPECIFIED    # audit: <schema path>@<commit>  |  design: <design-ref>
---

# Data model — {{SYSTEM}}

> **Mode.** `audit` = models observed in the schema. `design` = models to be built.
> **Status vocabulary.** `CONFIRMED` · `PARTIAL` · `ABSENT` · `UNSPECIFIED` · `UNVERIFIED`
> **Tenant field** is declared in frontmatter once and referenced throughout. If the system has no tenant concept, set it to `n/a` and say so in §1.

---

## 1. Model summary

Read first by the boundary trace. One row per model.

| ID | Model | Tenant-scoped | Tenant field present | Holds sensitive data | Status | Evidence |
|---|---|---|---|---|---|---|
| M-1 | | | | | | |

**Column vocabulary**

- **Tenant-scoped** — `yes` (this model's rows belong to one tenant) / `no` (global or reference data) / `UNSPECIFIED`.
- **Tenant field present** — `yes` / `NO-TENANT-FIELD` / `n/a`.
- A row reading `Tenant-scoped: yes` with `NO-TENANT-FIELD` is the pattern the boundary trace starts from. Record it. Do not assign severity here.

---

## 2. Model detail

Repeat this block per model.

### M-n — {{ModelName}}

**Purpose.** One line.

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|

**Relations**

| Relation | Target model | Cardinality | Cascade behavior | Evidence |
|---|---|---|---|---|

**Tenant scoping.** How a row is attributed to a tenant. Field name, or the relation path that reaches one. `NO-TENANT-FIELD` if neither exists.

**Access pattern.** Which routes read or write this model. Reference route IDs from `routes.md`.

---

## 3. Ownership and identity

| Concern | Model / field | Status | Evidence |
|---|---|---|---|
| User identity | | | |
| Tenant / organization entity | | | |
| User-to-tenant membership | | | |
| Role or permission storage | | | |
| Session storage | | | |

If membership is many-to-many, say so. It changes what "the tenant" means in a session.

---

## 4. Migrations and drift

| Item | Observation | Status | Evidence |
|---|---|---|---|
| Migration history present | | | |
| Schema matches migrations | | | |
| Manual schema changes evident | | | |

**design mode:** record the intended migration discipline instead.

---

## 5. Coverage

| Measure | Count |
|---|---|
| Total models | |
| Tenant-scoped: yes | |
| Of those, `NO-TENANT-FIELD` | |
| Holding sensitive data | |

---

## 6. Open items

| ID | Item | Why unresolved | Blocks |
|---|---|---|---|
