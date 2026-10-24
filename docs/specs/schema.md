---
doc: schema
mode: design
system: CSFLite
tenant_field: organization_id
version: 0.1
date: 2026-10-24
source: docs/specs/design/phase-4-web-interface.md §8, docs/specs/adr/ADR-0009-tenant-ready-data-model.md
---

# Data model — CSFLite

> **Mode.** `design` = models to be built. Nothing here is implemented yet.
> **Status vocabulary.** `CONFIRMED` · `PARTIAL` · `ABSENT` · `UNSPECIFIED` · `UNVERIFIED`
> **Tenant field.** `organization_id`. A tenant is one assessed organization.
> **Phases.** `MVP` models ship with the single-tenant Phase 4 web app. `MT` models ship with the hosted multi-tenant release. The MVP seeds exactly one Organization row. No MVP table changes shape when the `MT` models arrive.
> **Binding.** No. The spec brief remains the contract. This extends design §8, which lists four models, and is recorded in ADR-0009.

---

## 1. Model summary

| ID | Model | Phase | Tenant-scoped | Tenant field present | Holds sensitive data | Status | Evidence |
|---|---|---|---|---|---|---|---|
| M-1 | Organization | MVP | n/a. It is the tenant | n/a | yes. The name identifies the organization | CONFIRMED | ADR-0009 |
| M-2 | Assessment | MVP | yes | yes | yes. The label identifies the organization | CONFIRMED | design §8, ADR-0009 |
| M-3 | Response | MVP | yes | yes | yes. Control gaps and free-text notes | CONFIRMED | design §8, ADR-0009 |
| M-4 | Evidence | MVP | yes | yes | yes. Organization documents | CONFIRMED | design §8, ADR-0009 |
| M-5 | Result | MVP | yes | yes | yes. Scored output | CONFIRMED | design §8, ADR-0009 |
| M-6 | User | MT | no. Global identity, reaches a tenant through M-7 | n/a | yes. Email address | CONFIRMED | ADR-0009 |
| M-7 | Membership | MT | yes | yes | no | CONFIRMED | ADR-0009 |
| M-8 | ExternalIdentity | MT | no. Reaches a tenant through M-6 and M-7 | n/a | yes. Links a person to a provider account | CONFIRMED | ADR-0009 |
| M-9 | Invitation | MT | yes | yes | yes. Email address | CONFIRMED | ADR-0009 |
| M-10 | AuditLog | MT | yes | yes | no. Holds ids and action names, not content | CONFIRMED | ADR-0009, closes OI-8 in architecture.md |

Reference data (the 25 subcategories, weights, recommendations) is not a model. It stays in `data/csf_lookup.csv` (ADR-0004) and is shared by every tenant.

---

## 2. Model detail

All primary keys are UUIDs. All timestamps are timezone-aware UTC.

### M-1 — Organization

**Purpose.** The tenant. One assessed organization.

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|
| id | UUID | PK | no | |
| name | text | required | yes | |
| slug | text | unique | no | URL-safe name |
| status | text | `active` or `suspended` | no | |
| created_at | timestamp | required | no | |

**Relations**

| Relation | Target model | Cardinality | Cascade behavior | Evidence |
|---|---|---|---|---|
| has | Assessment | 1 to many | RESTRICT. Deleting an organization that still has data is blocked | ADR-0009 |
| has | Membership, Invitation, AuditLog | 1 to many | RESTRICT | ADR-0009 |

**Tenant scoping.** It is the tenant.

**Access pattern.** MVP: seeded once at startup, never edited through a route. MT: created by the platform operator, not by tenants.

### M-2 — Assessment

**Purpose.** One engagement for one organization. An organization can have many over time.

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|
| id | UUID | PK | no | |
| organization_id | UUID | FK to Organization, required | no | Tenant key |
| label | text | required | yes | |
| status | text | `draft`, `in_progress` or `completed` | no | |
| created_at | timestamp | required | no | |
| completed_at | timestamp | nullable | no | Empty until completed |

Unique on (organization_id, id). Child tables use this pair as their foreign key target.

**Relations**

| Relation | Target model | Cardinality | Cascade behavior | Evidence |
|---|---|---|---|---|
| belongs to | Organization | many to 1 | RESTRICT | ADR-0009 |
| has | Response | 1 to 25 | CASCADE | design §8 |
| has | Result | 1 to many | CASCADE | ADR-0009 |

**Tenant scoping.** `organization_id`.

### M-3 — Response

**Purpose.** The answer to one of the 25 questions in one assessment.

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|
| id | UUID | PK | no | |
| organization_id | UUID | required | no | Tenant key |
| assessment_id | UUID | required | no | |
| csf_subcategory_id | text | required | no | Such as `GV.OC-01`. Validated against `csf_lookup.csv` by the app, not a foreign key |
| response | text | `Yes`, `Partial` or `No`. Nullable | yes | Empty until answered. Scoring and Result generation require all 25 answered |
| notes | text | | yes | Not read by scoring or exports (design §8) |
| updated_at | timestamp | required | no | |

Unique on (assessment_id, csf_subcategory_id). Composite foreign key (organization_id, assessment_id) to Assessment (organization_id, id).

**Relations**

| Relation | Target model | Cardinality | Cascade behavior | Evidence |
|---|---|---|---|---|
| belongs to | Assessment | many to 1 | CASCADE | design §8 |
| has | Evidence | 1 to many | CASCADE | design §8 |

**Tenant scoping.** `organization_id`, kept equal to the parent's by the composite foreign key.

### M-4 — Evidence

**Purpose.** One uploaded file attached to a response. Scoring ignores it (design §8).

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|
| id | UUID | PK | no | |
| organization_id | UUID | required | no | Tenant key |
| response_id | UUID | required | no | |
| file_key | text | required, unique | no | Storage path `org/<organization_id>/<random>`. No original name in the path |
| original_filename | text | required | yes | Database only |
| size_bytes | integer | at most 26,214,400 | no | 25 MB cap (design §8) |
| uploaded_at | timestamp | required | no | |

Composite foreign key (organization_id, response_id) to Response (organization_id, id), so Response also carries a unique pair on (organization_id, id).

**Relations**

| Relation | Target model | Cardinality | Cascade behavior | Evidence |
|---|---|---|---|---|
| belongs to | Response | many to 1 | CASCADE for the row. The stored file is deleted by the application | design §8 |

**Tenant scoping.** `organization_id`, and the first segment of `file_key`.

### M-5 — Result

**Purpose.** Immutable scored snapshot of an assessment.

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|
| id | UUID | PK | no | |
| organization_id | UUID | required | no | Tenant key |
| assessment_id | UUID | required | no | |
| assessment_json | JSON | required | yes | |
| heatmap_json | JSON | required | yes | |
| lookup_digest | text | required | no | SHA-256 of `csf_lookup.csv` as loaded at boot |
| generated_at | timestamp | required | no | |

Rows are never updated. An assessment can have many; the latest by `generated_at` is the current one. Composite foreign key (organization_id, assessment_id) to Assessment.

**Tenant scoping.** `organization_id`.

### M-6 — User (MT)

**Purpose.** A person who signs in. Django's built-in user model.

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|
| id | UUID | PK | no | |
| email | text | unique, case-insensitive | yes | |
| name | text | | yes | |
| is_active | boolean | required | no | |
| created_at | timestamp | required | no | |

No password is stored. Login is by single sign-on only (ADR-0009).

**Tenant scoping.** Through Membership. A user has exactly one.

### M-7 — Membership (MT)

**Purpose.** Which organization a user belongs to, and the role there.

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|
| id | UUID | PK | no | |
| user_id | UUID | FK to User, **unique** | no | One organization per user for now |
| organization_id | UUID | FK to Organization, required | no | Tenant key |
| role | text | `owner`, `assessor` or `viewer` | no | |
| created_at | timestamp | required | no | |

The unique rule on `user_id` is the only thing that makes this one-to-one. Dropping it later allows many organizations per user. No other table would change.

### M-8 — ExternalIdentity (MT)

**Purpose.** Links a user to an account at an identity provider.

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|
| id | UUID | PK | no | |
| user_id | UUID | FK to User, required | no | |
| provider | text | `google` or `microsoft` | no | |
| subject_id | text | required | yes | The provider's stable id for the person |
| email_at_login | text | | yes | For display only. Never used as a key |
| created_at | timestamp | required | no | |

Unique on (provider, subject_id). Login matches on this pair, never on email, after the first sign-in.

### M-9 — Invitation (MT)

**Purpose.** Permission for a named person to join an organization. Joining is by invitation only.

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|
| id | UUID | PK | no | |
| organization_id | UUID | FK to Organization, required | no | Tenant key |
| email | text | required | yes | |
| role | text | `owner`, `assessor` or `viewer` | no | |
| status | text | `pending`, `accepted`, `revoked` or `expired` | no | |
| expires_at | timestamp | required | no | |
| created_by | UUID | FK to User | no | |
| created_at | timestamp | required | no | |

Unique pending invitation per (organization_id, lower(email)). On first sign-in, the app matches the verified email from the provider to a pending invitation and creates the Membership.

### M-10 — AuditLog (MT)

**Purpose.** Append-only record of who did what.

| Field | Type | Constraints | Sensitive | Notes |
|---|---|---|---|---|
| id | UUID | PK | no | |
| organization_id | UUID | required | no | Tenant key |
| actor_user_id | UUID | nullable | no | Empty for system actions |
| action | text | required | no | For example `response.updated`, `evidence.downloaded` |
| target_type, target_id | text, UUID | | no | |
| occurred_at | timestamp | required | no | |

Rows are never updated or deleted by the application.

---

## 3. Ownership and identity

| Concern | Model / field | Status | Evidence |
|---|---|---|---|
| User identity | M-6 User, MT. MVP has none | CONFIRMED | ADR-0009, ADR-0007 for the MVP |
| Tenant / organization entity | M-1 Organization. One seeded row in the MVP | CONFIRMED | ADR-0009 |
| User-to-tenant membership | M-7 Membership. One organization per user, enforced by a unique rule on `user_id`. Not many-to-many | CONFIRMED | ADR-0009 |
| Role or permission storage | `Membership.role`: owner, assessor, viewer | CONFIRMED | ADR-0009 |
| Session storage | Django sessions. The active organization is derived from the user's Membership, not chosen | PARTIAL. Backend (database or signed cookie) is UNSPECIFIED | ADR-0009 |

The seam: one function, `current_organization(request)`. The MVP returns the seeded row. MT returns the signed-in user's Membership organization. Every query, file download and export goes through it.

---

## 4. Migrations and drift

Intended discipline (design mode).

| Item | Intent | Status | Evidence |
|---|---|---|---|
| Migration history | Django migrations, run as an explicit release step, never on app boot | CONFIRMED | design §12 |
| MVP migration | Creates M-1 to M-5 and seeds one Organization | CONFIRMED | ADR-0009 |
| MT migration | Adds M-6 to M-10 only. It does not alter M-1 to M-5 | CONFIRMED | ADR-0009 |
| Composite foreign keys | Django's ORM cannot declare them. Added by `RunSQL` in the migration, with a reverse. The model code also checks the pair | PARTIAL. Needs a test on both SQLite and PostgreSQL | OI-S1 |
| SQLite foreign keys | Foreign key enforcement is on (Django's default) | UNVERIFIED | Confirm with a test |
| Row-level security | PostgreSQL only, added in the MT release by policy on `organization_id`. No schema change needed | ABSENT | ADR-0009 |
| Manual schema changes | Not allowed. Every change is a migration | CONFIRMED | design §12 |

---

## 5. Coverage

| Measure | Count |
|---|---|
| Total models | 10 |
| Built in the MVP | 5 |
| Tenant-scoped: yes | 7 (M-2, M-3, M-4, M-5, M-7, M-9, M-10) |
| Of those, `NO-TENANT-FIELD` | 0 |
| Reach a tenant only through another model | 2 (M-6, M-8) |
| Holding sensitive data | 8 (M-1, M-2, M-3, M-4, M-5, M-6, M-8, M-9) |

---

## 6. Open items

| ID | Item | Why unresolved | Blocks |
|---|---|---|---|
| OI-S1 | Composite foreign keys need raw SQL in migrations | Django has no ORM support. Needs a test on SQLite and PostgreSQL | MVP build |
| OI-S2 | Evidence download must check the file's organization, not only that the user is signed in | Route design not written. TB-5 in architecture.md covers the browser boundary only | MT release |
| OI-S3 | Weights and recommendations are shared by all tenants | Per-tenant reference data would need a different design | none |
| OI-S4 | Organization offboarding: export and deletion of a tenant's data and files | RESTRICT blocks deletion today. No procedure written | MT release |
| OI-S5 | `django-allauth` support for Django 5.2 is not verified. SAML is not planned | Version must be pinned under AD-11 after a smoke test | MT release |
| OI-S6 | Session backend and cookie flags (architecture.md OI-4) | Not decided | MT release |
| OI-S7 | Login rate limiting (architecture.md OI-5). Less urgent with SSO only, but invitations and callbacks are still public routes | Not decided | MT release |
| OI-S8 | `architecture.md` TB-2 and TB-3 say `n/a`. They become real boundaries in the MT release | Update when the MT release is designed | MT release |
| OI-S9 | Audit log retention and who can read it | Not decided | MT release |
