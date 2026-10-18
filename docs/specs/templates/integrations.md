---
doc: integrations
mode: audit            # audit | design
system: UNSPECIFIED
version: 0.1
date: YYYY-MM-DD
source: UNSPECIFIED    # audit: <repo>@<commit>  |  design: <design-ref>
---

# Integrations — {{SYSTEM}}

> **Mode.** `audit` = integrations observed in source. `design` = integrations to be built.
> **Status vocabulary.** `CONFIRMED` · `PARTIAL` · `ABSENT` · `UNSPECIFIED` · `UNVERIFIED`
> **Credential rule — absolute.** Environment variable **names** only. Never a value, never a fragment of one, in either mode.
> **Named services only.** Specific product names. `UNSPECIFIED` where the repo does not identify it.

---

## 1. Inventory

| ID | Service | Purpose | Direction | Credential env var name | Credential type | Status | Evidence |
|---|---|---|---|---|---|---|---|
| I-1 | | | | | | | |

**Column vocabulary**

- **Direction** — `outbound` (we call them) / `inbound` (they call us) / `bidirectional`.
- **Credential type** — `api-key` / `oauth` / `service-account` / `webhook-secret` / `none` / `UNSPECIFIED`.

---

## 2. Integration detail

Repeat per integration.

### I-n — {{ServiceName}}

| Attribute | Value |
|---|---|
| Purpose | |
| Direction | |
| Protocol / transport | |
| Credential env var name | |
| Credential scope | |
| Where credential is configured | |
| Token storage (if OAuth) | |
| Token refresh handling | |
| Failure behavior | |
| Status | |
| Evidence | |

**Data crossing the boundary.** What leaves, what arrives. Reference data classes from `architecture.md` §6.

**Tenant attribution.** If this integration handles tenant data, how is the tenant determined on each call? Reference the tenant field from `schema.md`.

---

## 3. Inbound endpoints

Webhooks and callbacks. Each one is an unauthenticated entry point until proven otherwise.

| ID | Service | Path | Signature verification | Replay protection | Status | Evidence |
|---|---|---|---|---|---|---|

Cross-reference these paths against `routes.md` §2.

---

## 4. Credential surface

Every env var name the system expects. Names only.

| Env var name | Used by | Required | Declared in | Status |
|---|---|---|---|---|

**Declared in** — `.env.example`, config schema, or `UNDECLARED`. An undeclared variable read at runtime is worth recording.

---

## 5. Coverage

| Measure | Count |
|---|---|
| Total integrations | |
| Holding a credential | |
| OAuth token storage present | |
| Inbound endpoints | |
| Inbound with signature verification | |

---

## 6. Open items

| ID | Item | Why unresolved | Blocks |
|---|---|---|---|
