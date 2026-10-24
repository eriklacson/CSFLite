# ADR-0009: Build a Single-Tenant MVP on a Tenant-Ready Data Model

## Status

Accepted

## Date

2026-10-24

## Context

The Phase 4 MVP has one operator and no tenants (ADR-0006, ADR-0007). A multi-tenant release is
planned. It runs the same container image, deployed once in the cloud and shared by many tenants.
The tenant is each assessed organization. Only that organization's own staff sign in.

The Phase 4 design lists four models and no organization record. The only trace of the assessed
organization is the free-text `Assessment.label`. Adding a tenant key to every table later means a
migration on each table, and a single query that misses the filter leaks one tenant's data to
another.

## Decision

**Tenant key on every table.** Every table below Organization carries `organization_id`. The MVP
seeds exactly one Organization row.

**The database enforces the key.** Child rows point to their parent by the pair
(`organization_id`, parent id). A Response cannot belong to a different organization than its
Assessment.

**UUID primary keys.** Ids stay unique if data is moved or merged.

**One seam for the current organization.** All queries, file downloads and exports go through
`current_organization(request)`. The MVP returns the seeded row. The multi-tenant release returns
the signed-in user's organization.

**Evidence paths start with the organization id.** Storage permissions can then be scoped per
tenant.

**Results are snapshots, and can be many.** Each assessment can hold several, and the latest is
current. `Response.response` is empty until answered. Scoring needs all 25 answered.

**Identity arrives with the multi-tenant release, not before.** The release adds User, Membership,
ExternalIdentity, Invitation and AuditLog. It does not alter the five MVP tables.

- Single sign-on only, through Google and Microsoft work accounts. No passwords are stored.
- A user belongs to one organization. A unique rule on `Membership.user_id` enforces it.
- Joining is by invitation. No automatic joining by email domain.
- Login matches the provider's subject id, never the email, after the first sign-in.
- The first release sends no email. The owner registers a colleague's email and tells them to sign in.

Reference data stays in `csf_lookup.csv` and is shared by every tenant (ADR-0004).

## Consequences

**Positive:**
- Moving to multi-tenant adds tables. It does not rewrite the MVP tables.
- Postgres row-level security can be switched on later with no schema change.
- A mismatched parent and child is impossible, not just unlikely.

**Negative / trade-offs:**
- Django's ORM cannot declare composite foreign keys. They are added with raw SQL in migrations and
  need a test on both SQLite and PostgreSQL.
- Every MVP table carries a column the MVP does not use.
- Weights and recommendations cannot differ by tenant.
- Single sign-on only means staff with no Google or Microsoft work account cannot join.

**Superseded when the multi-tenant release ships:**
- ADR-0006 "never offered as a hosted service" no longer holds for that profile.
- ADR-0007 one shared password no longer applies to that profile.
- The local profile and the MVP are unchanged.

## Alternatives Considered

**Tenant key on Assessment only.** Rejected. Tenant filtering then needs joins everywhere, row-level
security is harder, and a missed join leaks data.

**Integer ids.** Rejected. They collide on merge and reveal how many rows exist.

**A database or schema per tenant.** Rejected for now. More operational work per tenant, and the
tenants are small.

**Many organizations per user.** Rejected. Staff-only tenancy does not need it. The unique rule
can be dropped later.

**Automatic joining by email domain.** Rejected. Shared domains such as gmail.com and one
configuration mistake would give a stranger access to a tenant.

**Passwords alongside single sign-on.** Rejected. It adds reset and guessing risks for little gain.

**Add the tenant key when multi-tenant starts.** Rejected. It is the migration this ADR avoids.
