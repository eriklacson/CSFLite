---
plan: scope-template-check
scope_doc: none yet   # approved exception (decision 1). See "Decisions".
status: approved
round_limit: 3
---

# Plan scope-template-check — Make every scope file follow the scope template

> Draft. Not approved. Do not start IMPLEMENT until the architect runs `harness/loop/approve.sh scope-template-check`, which moves this folder to `harness/plans/scope-template-check/`.
> After approval only the Status column changes, and only `mark-done.sh` changes it.

## What this plan delivers

A check that every scope file follows `docs/scopes/template.scope.md`. Approval is refused when a plan's scope fails it. Pre-commit and CI run it too. The Phase 4 scope is converted to the template in place (option A).

## The change in plain words

- One validator: `harness/loop/scope-check.sh`. It lives in `planlib.py`, next to `approve.sh` and `mark-done.sh`.
- The template is the only source. The validator reads the frontmatter keys, the section headings and the table columns from `docs/scopes/template.scope.md`. Change the template, and the check follows.
- A scope file is found by its frontmatter `doc: scope`, not by its folder. The Phase 4 scope keeps its name and location.
- It checks structure, not quality. Whether a criterion is really checkable stays a person's call (P-7).
- Nothing in the product depends on it. The validator and its tests live in `harness/`. They are not in `tests/`, so deleting `harness/` still leaves a project that builds.

## What the validator checks

| ID | Check | Rule |
|---|---|---|
| V-1 | Frontmatter has every key the template has. `doc` is `scope`. `status` is `draft` or `ready for plan`. `scope` is a stub: lowercase letters, digits and hyphens. | P-11, P-10 |
| V-2 | The six `##` section headings appear exactly as in the template, in the same order. No other `##` heading. | P-11 |
| V-3 | Each section's table has the template's columns, in order. | P-11 |
| V-4 | Section 3 has at least one success criterion. Section 4 has at least one deliverable. | P-5 |
| V-5 | Every success criterion has a filled "Checked by" cell: a command, a check reference, or `human`. | P-6 |
| V-6 | IDs are unique within the file and use the template's prefixes: `SC-n`, `D-n`, `NG-n`. | P-11 |
| V-7 | Each "Rows it covers" row names a record file that exists, and that file contains the row ID. | P-4 |
| V-8 | The template file itself is skipped. | — |

The stub check (V-1) does not require the two-digit number from the template's example. CSFLite stubs do not use one (`phase4-descope`, `spec-brief-components`).

## Tasks

Do the tasks in order. A task starts only when every task it depends on is `done`.

| ID | Task | Depends on | Check | Round limit | Status |
|---|---|---|---|---|---|
| T-1 | Write the validator tests in `harness/loop/tests/test_scope_check.py`. Cover V-1 to V-8, `--all` discovery, and `approve.sh` refusing a missing or failing `scope_doc`. Use small scope files built in `tmp_path`. Run them: they must fail, because nothing is built. Add the harness tests to Ruff's per-file ignores in `pyproject.toml`. | — | `bash harness/plans/scope-template-check/scope-template-check.check.sh T-1` | 3 | done |
| T-2 | Build `scope-check` in `harness/loop/planlib.py`, with the wrapper `harness/loop/scope-check.sh <file> \| --all`. Exit 0 pass, 1 fail, 2 usage. `--all` checks every tracked file with `doc: scope`, and every draft or approved plan's `scope_doc` that is a file. | T-1 | `bash harness/plans/scope-template-check/scope-template-check.check.sh T-2` | done | todo |
| T-3 | In `approve`, before anything moves: refuse (exit 4) if the plan's `scope_doc` is missing, is not a file, or fails `scope-check`. Print the failing checks. | T-2 | `bash harness/plans/scope-template-check/scope-template-check.check.sh T-3` | 3 | done |
| T-4 | Convert `docs/specs/phase-4/web-interface-scope.md` to the template, in place. Keep every bullet's text. Use the mapping and the proposed tables below. | T-2 | `bash harness/plans/scope-template-check/scope-template-check.check.sh T-4` | 3 | done |
| T-5 | Run `scope-check.sh --all` in pre-commit (hook id `scope-check`) and in CI. Add a CI step that runs `python -m pytest -q harness/loop/tests`. | T-3, T-4 | `bash harness/plans/scope-template-check/scope-template-check.check.sh T-5` | 3 | todo |
| T-6 | Add rule P-11 to `harness/rules.md` and set P-5, P-6 and P-11 to `installed`. Add `scope-check.sh` to `harness/loop/README.md`. In `AGENTS.md`, say that scope files are found by `doc: scope`. | T-5 | `bash harness/plans/scope-template-check/scope-template-check.check.sh T-6` | 3 | todo |

## Mapping for T-4: old sections to template sections

| Old section | Goes to |
|---|---|
| Header lines (Source, Full design, Scope change, Status) and "spec brief wins" | A blockquote under the title |
| What Phase 4 is | §1 What this scope delivers |
| In scope | §4 Deliverables, one row per bullet (D-1 to D-8) |
| What is retired | §4 Deliverables (D-9 to D-11) |
| Out of scope for Phase 4 | §5 Not in this scope, one row per bullet (NG-1 to NG-6) |
| What carries over unchanged | §5 Not in this scope (NG-7 to NG-9), with the reason "carries over unchanged" |
| Acceptance | §3 Success criteria, one row per bullet (SC-1 to SC-6) |
| (none) | §2 Rows it covers: see proposal below |
| (none) | §6 Open items: empty table |

Frontmatter: `scope: phase4-web-interface`, `spec_outcomes: []`, `status: ready for plan`.

## "Checked by" for the six criteria (approved, decision 4)

| SC | Criterion (text kept) | Checked by |
|---|---|---|
| SC-1 | An assessment completes end to end in the browser | Browser acceptance test (design §17). Test path open: G-8 |
| SC-2 | Web output is byte-identical to `tests/fixtures/golden/` | INV-9: `tests/test_golden_pipeline.py`, web extension |
| SC-3 | The container starts from `docker compose up` with no host Python | INV-15 and INV-26: compose acceptance test |
| SC-4 | A past result does not change when `csf_lookup.csv` is reweighted | INV-8: reweighting acceptance test |
| SC-5 | Evidence only through the app, and never changes a score | INV-11: download test. INV-6: golden test with evidence attached |
| SC-6 | Public mode refuses to start without a password, and redirects HTTP to HTTPS | INV-14 (b): startup test. INV-30: redirect test |

Most of these tests do not exist yet. P-6 only asks that the cell is filled. Each cell names the standards row that holds the mechanism, so no new rule is invented.

## "Rows it covers" (approved, decision 4)

Every CO and INV row in `docs/specs/standards.md`, except INV-16 (deferred to Phase 7 by ADR-0011) and CO-2 (no rule yet, G-8). `standards.md` states its scope as the Phase 4 web application, so this is derived, not chosen.

## How the tasks cover the scope

No scope doc exists for this plan (decision 1). These are the plan's own criteria.

| Criterion | Task |
|---|---|
| The validator enforces V-1 to V-8 | T-1, T-2 |
| Approval is refused when the scope fails | T-1, T-3 |
| The Phase 4 scope passes, with no bullet lost | T-4 |
| Pre-commit and CI run the check | T-5 |
| The rule and the docs say what is enforced | T-6 |

## Rules from the standards record

| Rule | How it is checked |
|---|---|
| P-1 A task is done only when its check passes | `check.sh` exit code, through `mark-done.sh` |
| P-5, P-6 | Become `installed` through V-4 and V-5 at approval |
| CO-11 Black, Ruff, Bandit pass | Gate G-4 |
| Files in `docs/` change only if the approved plan lists them | Only `docs/specs/phase-4/web-interface-scope.md` changes. T-4 checks it. |

## Files this plan changes

- `harness/loop/planlib.py`, `harness/loop/scope-check.sh` (new), `harness/loop/tests/test_scope_check.py` (new), `harness/loop/README.md`
- `harness/rules.md`
- `docs/specs/phase-4/web-interface-scope.md`
- `.pre-commit-config.yaml`, `.github/workflows/python-lint.yaml`, `pyproject.toml` (Ruff per-file ignores only)
- `AGENTS.md`

## Not in this plan

- **The plan-building skill and the reviewer subagent.** They come next and use this check.
- **Carrying the check over to jig.** After CSFLite proves it. Tracked in eriklacson/jig#6.
- **The tests hash.** `stop-check.sh` is not built, so the T-1 tests are not hashed. A person confirms they failed first.
- **Checking quality.** Whether a criterion is really checkable stays with P-7, a person's judgment.
- **Schema and architecture rows in "Rows it covers".** Only standards rows for now (decision 4).

## Decisions

1. **No scope doc for this plan: approved as the last exception** (architect, 2026-11-28). This plan builds the scope check, so it has no scope file. After T-3, `approve.sh` refuses any plan without a valid scope. No later plan can skip one.
2. **`spec-brief-components` needs a scope before approval** (architect, 2026-11-28). No second exception. A scope file is written for it from the template before `approve.sh` runs on it.
3. **`phase4-descope` T-9 marked done on its own branch** (architect, 2026-11-28). `mark-done.sh` passed it on `refactor/phase4-descope`, in PR eriklacson/CSFLite#79. Once that merges, `approve.sh` can approve this plan. The REPORT stage for `phase4-descope` stays with the architect.
4. **The "Checked by" and "Rows it covers" tables are approved as proposed** (architect, 2026-11-28). Schema and architecture rows are left out until those records have row IDs a check can rely on.
5. **Branch: `harness/scope-template-check`** (architect, 2026-11-28). One plan stays on one branch. The prefix follows most of the work, which is harness work. T-4 is the only docs change.

## Open items for the architect

None.
