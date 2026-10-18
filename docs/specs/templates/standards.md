---
doc: standards
mode: audit            # audit | design
system: UNSPECIFIED
version: 0.1
date: YYYY-MM-DD
source: UNSPECIFIED    # audit: <repo>@<commit>  |  design: <design-ref>
stack_ref: UNSPECIFIED # architecture.md — the stack these rules are written against
---

# Standards — {{SYSTEM}}

> **Mode.** `audit` = rules observed to be enforced. `design` = rules to enforce.
> **Status vocabulary.** `CONFIRMED` · `PARTIAL` · `ABSENT` · `UNSPECIFIED` · `UNVERIFIED`
> **Install status.** `unbuilt` → `installed` → `proven` (fired on a real regression and held). Only `proven` validates the control.
> **Locus.** `[G]` generator governance · `[P]` pipeline gate · `[R]` assisted remediation. A rule with no locus does not survive regeneration.
> **Imperative voice.** Invariants are written as rules, not observations: "tenant id derives from the session", never "tenant id appears to derive from the session".

This file is authoritative for the rules of this system. Rules are stack-dependent, so they are written against the stack recorded in `architecture.md` §3. A rule carried over from another system is re-stated here against this stack or it does not apply.

---

## 1. Code organization

How the codebase is arranged. `architecture.md` §3 records what the stack is. This records how it must be laid out.

| ID | Convention | Applies to | Enforcement mechanism | Locus | Install status | Status | Evidence |
|---|---|---|---|---|---|---|---|
| CO-1 | Directory layout | repo | | | | | |
| CO-2 | Module boundaries | | | | | | |
| CO-3 | Where business logic lives | | | | | | |
| CO-4 | Where data access lives | | | | | | |
| CO-5 | Naming conventions | | | | | | |
| CO-6 | Shared / generated code handling | | | | | | |
| CO-n | | | | | | | |

**audit mode:** record the layout as found, including where it is inconsistent.
**design mode:** this is what the generator follows. A convention with no mechanism will drift on the next regeneration.

---

## 2. Invariants

Rules the system must not violate. Each needs a mechanism and a locus, or it is a wish.

| ID | Invariant | Scope | Enforcement mechanism | Locus | Install status | Status | Evidence |
|---|---|---|---|---|---|---|---|
| INV-1 | Tenant identity derives from the authenticated session, never from request input | all tenant-scoped routes | | | | | |
| INV-2 | Tenant scoping is applied in the query layer, not in the handler | all tenant-scoped queries | | | | | |
| INV-3 | Untrusted input is validated at the boundary before reaching any sink | all input-handling routes | | | | | |
| INV-4 | No secret value exists in source or in git history | repo | | | | | |
| INV-5 | A change reaching production has passed a required check at the merge point | pipeline | | | | | |
| INV-n | | | | | | | |

**audit mode:** `Install status` is read from what exists. Most rows will be `unbuilt`. That is the finding.
**design mode:** every invariant ships with a named mechanism and locus before the first feature.

**Subtraction note.** Where an invariant is enforced by removing a path rather than guarding it, record the removal as the mechanism. A deleted client-trust path cannot regress.

---

## 3. Failure semantics

What the system does when something breaks. Per-service failure behavior lives in `integrations.md`; this is system-level.

| ID | Failure mode | Trigger | Detection | Behavior | User-visible result | Recovery | Status | Evidence |
|---|---|---|---|---|---|---|---|---|
| F-1 | Auth provider unreachable | | | | | | | |
| F-2 | Database unreachable | | | | | | | |
| F-3 | External integration timeout | | | | | | | |
| F-4 | Unhandled exception in a handler | | | | | | | |
| F-n | | | | | | | | |

**Behavior vocabulary** — `fail-closed` / `fail-open` / `degrade` / `retry` / `queue` / `UNSPECIFIED`.

A security-relevant path that fails open is a finding, not a design choice, unless a decision record says otherwise. Reference the AD- id from `architecture.md` §7.

---

## 4. Error and logging posture

| Concern | Rule | Enforcement | Status | Evidence |
|---|---|---|---|---|
| Error detail returned to client | | | | |
| Stack traces in responses | | | | |
| Secrets or tokens in logs | | | | |
| PII in logs | | | | |
| Tenant id in log context | | | | |
| Log retention | | | | |

---

## 5. Environment matrix

| Environment | Purpose | Data | Auth posture | Publicly reachable | Deploy trigger | Status | Evidence |
|---|---|---|---|---|---|---|---|
| local | | | | | | | |
| preview | | | | | | | |
| staging | | | | | | | |
| production | | | | | | | |

**Data vocabulary** — `synthetic` / `anonymized` / `production-copy` / `production` / `UNSPECIFIED`.

A preview or staging environment carrying production data while publicly reachable is the pairing to look for. Record both columns even when one is `UNSPECIFIED`.

---

## 6. Rate and resource limits

| Scope | Limit | Enforcement point | Status | Evidence |
|---|---|---|---|---|
| Unauthenticated endpoints | | | | |
| Authenticated endpoints | | | | |
| Expensive operations | | | | |
| Upload size | | | | |
| Query result size / pagination | | | | |

Unbounded pagination on a tenant-scoped query is both a resource limit and a boundary concern. Cross-reference `routes.md`.

---

## 7. Coverage

| Measure | Count |
|---|---|
| Code conventions declared | |
| With a named mechanism | |
| Invariants declared | |
| With a named mechanism | |
| With a locus assigned | |
| Install status: installed | |
| Install status: proven | |
| Failure modes with defined behavior | |
| Security-relevant paths failing open | |

Counts only. Coverage and sequencing stay on separate axes.

---

## 8. Open items

| ID | Item | Why unresolved | Owner | Blocks |
|---|---|---|---|---|
