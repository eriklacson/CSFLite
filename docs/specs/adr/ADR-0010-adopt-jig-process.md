# ADR-0010: Adopt the jig Process Without a Ruleset

## Status

Accepted (architect, 2026-11-08)

## Date

2026-11-08

## Context

CSFLite already runs a six-stage loop written in `AGENTS.md`: READ, PLAN, APPROVE, IMPLEMENT, VERIFY, REPORT.
Nothing enforces it.

jig is a boilerplate with the same six stages. It adds approved plans that cannot be edited, tests that are
locked by hash, and checks that decide when a task is done. jig's enforcement scripts (`mark-done.sh`,
`stop-check.sh`, `gate.sh`) are not built yet.

jig expects every project to pick one ruleset. Its `lean-security` ruleset is written for multi-tenant SaaS.
CSFLite Phase 4 has no tenants. `docs/specs/standards.md` already holds CSFLite's software rules.

## Decision

1. Adopt jig's process files: `harness/`, `VOCABULARY.md`, `.claude/`, and the scope template.
2. Use no jig ruleset. `docs/specs/standards.md` stays the only source of software rules.
3. Map jig terms to existing CSFLite files. Do not move or rename them (see `AGENTS.md`).
4. Rules from `lean-security` that CSFLite lacks were added to `standards.md` and approved on 2026-11-08:
   CO-20, INV-28, INV-29, and mechanisms on INV-18, F-4 and two logging rows.
5. Open gap G-22 (page size) is not filled from the ruleset. It stays with the architect.

## Consequences

**Positive:**
- One process, written once, with a path to enforcement when jig's scripts exist.
- No cross-reference in `docs/specs/` breaks.
- Software rules have one home.

**Negative / trade-offs:**
- Until jig's scripts are built, the jig rules are guidance only.
- jig files that mention a ruleset read oddly in CSFLite. `AGENTS.md` says to read it as `standards.md`.
- jig is adaptable and not enforced, so CSFLite can use it without a ruleset. No jig change is needed for that.

## Alternatives Considered

- **Use `lean-security`.** Rejected. Its build rules are about tenants, roles and webhooks, which Phase 4 does
  not have. Its reporting rules mostly repeat CSFLite's own.
- **Move `docs/specs/` into jig's layout.** Rejected. It would break many cross-references for no gain yet.
