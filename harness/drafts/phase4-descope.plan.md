---
plan: phase4-descope
scope_doc: docs/specs/phase-4/web-interface-scope.md
status: draft
round_limit: 3
---

# Plan phase4-descope — Cut Phase 4 to the container; move hosted profiles to Phase 7

> Draft. Not approved. Do not start IMPLEMENT until the architect approves and moves the three files into `harness/plans/`.

## What this plan delivers

The Phase 4 records describe one container image, run locally or on a network the operator controls. Every hosted profile moves to Phase 7, which starts only when usage justifies it.

## The change in plain words

**Stays in Phase 4**

- The Django app: questionnaire, evidence upload, report, heatmap, CSV export, CSV import.
- One container image. The local `docker compose` profile, published on `127.0.0.1`.
- Public mode (ADR-0007): `CSFLITE_PUBLIC`, `CSFLITE_PASSWORD`, `/login`, both startup guards.
- Network runs. An operator may run the container on a network or in their own cloud account. CSFLite supports this but ships no template or provisioning for it.
- SQLite and evidence files on disk, under `/data`. A network run needs `/data` on a persistent volume.
- `DATABASE_URL` stays as the setting that holds the SQLite path. Phase 4 tests SQLite only.
- CLI retirement and the golden parity gate.

**Moves to Phase 7**

- The DigitalOcean proof of concept: App Platform, Managed Postgres, Spaces, its environment template.
- Object storage: `django-storages`, `boto3`, `CSFLITE_STORAGE_BACKEND`, the `CSFLITE_S3_*` settings, the storage startup guard.
- Postgres and `psycopg`.
- AWS, Azure and GCP (already Phase 7).

**Phase numbers do not change.** Phase 5 stays Release Hardening. Phase 6 stays Community. Phase 7 is renamed from "Multi-Cloud Deployment Profiles" to "Hosted Deployment Profiles".

## Files this plan changes

Only these files in `docs/` may change. T-9 checks it.

| File | Task |
|---|---|
| `docs/specs/adr/ADR-0011-phase4-ships-container-only.md` (new) | T-1 |
| `docs/specs/adr/README.md` | T-1 |
| `docs/specs/adr/ADR-0006-self-hosted-container-delivery.md` | T-2 |
| `docs/specs/adr/ADR-0007-operator-declared-public-mode.md` | T-2 |
| `docs/specs/phase-4/web-interface-scope.md` | T-3 |
| `docs/specs/design/phase-4-web-interface.md` | T-4 |
| `docs/specs/csflite-spec-brief.md` | T-5 |
| `docs/development_roadmap.md` | T-6 |
| `docs/specs/architecture.md` | T-7 |
| `docs/specs/standards.md` | T-8 |
| `docs/specs/standards-gaps.md` | T-8 |

## Tasks

Do the tasks in order. A task starts only when every task it depends on is `done`.

The "cut rule" in the checks: a line that names a moved item (DigitalOcean, App Platform, Spaces, Managed Postgres, `CSFLITE_S3_*`, `CSFLITE_STORAGE_BACKEND`, `django-storages`, `boto3`, `psycopg`) must say `Phase 7` or `ADR-0011`, or sit under a heading that does.

| ID | Task | Depends on | Check | Round limit | Status |
|---|---|---|---|---|---|
| T-1 | Write ADR-0011 from the text in Appendix A, status Accepted, dated the approval day. Add it to the ADR index. | — | `bash harness/plans/phase4-descope.check.sh T-1` | 3 | todo |
| T-2 | Add a dated amendment to ADR-0006 and ADR-0007 that points to ADR-0011 (Appendix B). Add text only. Delete nothing. | T-1 | `bash harness/plans/phase4-descope.check.sh T-2` | 3 | todo |
| T-3 | Scope doc: remove the DigitalOcean profile from "In scope". Add network runs. Add the moved items to "Out of scope" under Phase 7. Drop the DigitalOcean acceptance line. Cite ADR-0011. | T-1 | `bash harness/plans/phase4-descope.check.sh T-3` | 3 | todo |
| T-4 | Design doc, per Appendix C: §1, §3, §7, §8, §9, §10, §11, §12, §13, §17, §18. | T-1 | `bash harness/plans/phase4-descope.check.sh T-4` | 3 | todo |
| T-5 | Spec brief: §7 Phase 4 paragraph, the §10 "Container is the only artifact" row, §12 delivery paragraph. Cite ADR-0011. | T-1 | `bash harness/plans/phase4-descope.check.sh T-5` | 3 | todo |
| T-6 | Roadmap: Phase 4 deliverables and acceptance criteria lose the DigitalOcean and storage items and gain network runs. Phase 7 is renamed "Hosted Deployment Profiles", gets the DigitalOcean proof of concept and the start condition from ADR-0011. Status table updated. | T-1 | `bash harness/plans/phase4-descope.check.sh T-6` | 3 | todo |
| T-7 | `architecture.md`, per Appendix D. | T-1 | `bash harness/plans/phase4-descope.check.sh T-7` | 3 | todo |
| T-8 | `standards.md` and `standards-gaps.md`, per Appendix E. Add gap G-25 (TLS for network runs). | T-1 | `bash harness/plans/phase4-descope.check.sh T-8` | 3 | todo |
| T-9 | Confirm only the files listed above changed in `docs/`, and the cut rule holds across `docs/` outside ADRs and checks. | T-2 to T-8 | `bash harness/plans/phase4-descope.check.sh T-9` | 3 | todo |

## How the tasks cover the scope

No scope doc exists in `docs/scopes/` for this change. It changes the Phase 4 scope summary itself. Rule P-9 needs an accepted decision record for a scope change. ADR-0011 is that record.

| Criterion | Task |
|---|---|
| The scope change has an accepted decision record (P-9) | T-1, T-2 |
| Phase 4 records name no hosted profile, object storage or Postgres, except as Phase 7 | T-3 to T-8 |
| Public mode and network runs stay in Phase 4 | T-3, T-4, T-8 |
| Phase 7 holds every hosted profile and a start condition | T-6 |
| Nothing outside the listed files changed | T-9 |

## Rules from the standards record

| Rule | How it is checked |
|---|---|
| P-1 A task is done only when its check passes | `check.sh` exit code |
| P-9 Every scope change has an accepted decision record | T-1 writes ADR-0011 as Accepted |
| `docs/` changes only where the approved plan lists the file | T-9 |
| CO-4 `assess_helpers.py` does not change | Gate G-3 (golden pipeline) |

## Not in this plan

- **Tenancy (G-1).** This cut makes the ADR-0009 tenant columns harder to justify in Phase 4. It is a separate decision.
- **`schema.md` OI-S1.** It asks for a composite foreign key test on SQLite and PostgreSQL. The PostgreSQL half now waits for Phase 7. OI-S1 is tenancy work under G-1, so it is left as is.
- **A network-run template.** Phase 4 documents network runs. It ships no compose override or cloud template for them. Shipping one would be building beyond scope.
- **Check records.** CHK-0001 to CHK-0004 are history and do not change.
- **Phase renumbering.** Rejected. See ADR-0011.

## Open items for the architect

1. **Phase 7 start condition.** Appendix A proposes: Phase 6's usage metric is met (3 organizations), or an operator asks for a hosted profile and agrees to test it. Approve or change.
2. **`DATABASE_URL`.** This plan keeps it as the SQLite path setting, so no new variable is invented. Self-deployers could point it at Postgres, but Phase 4 does not test that. Confirm, or say Postgres must be refused in Phase 4.
3. **TLS for network runs (new gap G-25).** DigitalOcean gave TLS for free. A network run now sends the operator password over whatever the operator sets up. This plan records the gap. It does not write a rule. A rule needs your decision.
4. **Approve the ADR-0011 text** in Appendix A, including the rejected alternatives.

---

## Appendix A — ADR-0011 text (for approval)

```markdown
# ADR-0011: Phase 4 Ships the Container Only; Hosted Profiles Wait for Usage

## Status

Accepted

## Date

<approval date>

## Context

Phase 4 included a DigitalOcean proof of concept: App Platform, Managed Postgres and Spaces.
Nobody uses CSFLite yet, so no user needs a hosted profile.

The proof of concept has real costs. DigitalOcean has no free tier for this shape. It adds
`django-storages`, `boto3` and `psycopg` to the image. `django-storages` is not confirmed on
Django 5.2 (architecture OI-11). It adds a storage startup guard, an environment template, and
open items on transport encryption and object storage failures.

Its value was to test the object storage path early (ADR-0006, 2026-10-22 amendment). That
value depends on someone needing a hosted profile.

## Decision

**Phase 4 ships one container image.** The local `docker compose` profile is the only profile
CSFLite ships.

**Network runs are supported, not provisioned.** An operator may run the container on a network
or in a cloud account they control. Public mode (ADR-0007) stays in Phase 4 for this:
`CSFLITE_PUBLIC=true`, `CSFLITE_PASSWORD`, and their domain in `CSFLITE_ALLOWED_HOSTS`. CSFLite
ships no template or provisioning for it.

**Storage is SQLite and the filesystem.** Both live under `/data`. A network run needs `/data`
on a persistent volume. `DATABASE_URL` stays as the setting that holds the SQLite path. Phase 4
tests SQLite only.

**Hosted profiles move to Phase 7, renamed "Hosted Deployment Profiles".** Phase 7 holds the
DigitalOcean proof of concept, object storage, Postgres, and the AWS, Azure and GCP profiles.

**Phase 7 starts when** Phase 6's usage metric is met (3 organizations), or an operator asks for
a hosted profile and agrees to test it.

The portability rules do not change. Configuration comes from the environment. Application code
does not call a provider API or branch on the provider.

## Consequences

**Positive:**
- Phase 4 is smaller. No `boto3`, `django-storages` or `psycopg`. No storage guard. No template.
- The `django-storages` support risk leaves Phase 4.
- No cloud cost before there is a user.

**Negative / trade-offs:**
- The object storage path is not tested until Phase 7.
- A network run depends on a persistent volume. A host with only temporary disk loses data.
  Such hosts are unsupported until Phase 7.
- TLS for a network run is the operator's job, and no rule says so yet (standards-gaps G-25).
- Operators who run on a network get documentation, not a template.

## Alternatives Considered

**Keep the DigitalOcean proof of concept in Phase 4.** Rejected. No user justifies the cost.

**Loopback-only Phase 4, with public mode deferred.** Rejected. Operators can usefully run the
container on a network or in their own cloud account now.

**Make cloud Phase 5 and renumber.** Rejected. "Phase 5" for the supplements is written into
ADR-0008, the design, the spec brief, `architecture.md` and `AGENTS.md`. Building cloud before
the release and community phases would also come before the usage that justifies it.

## Relationship to other ADRs

- ADR-0006: the delivery model stands. The timing in its 2026-10-22 amendment changes.
- ADR-0007: public mode stands. The hosted environment template moves to Phase 7.
```

## Appendix B — Amendments

**ADR-0006, under `## Amendments`:**

> **<approval date>.** Phase 4 ships no hosted profile ([ADR-0011](ADR-0011-phase4-ships-container-only.md)). The DigitalOcean proof of concept, object storage and Postgres move to Phase 7. An operator may still run the container on a network or in their own cloud account, with SQLite and evidence on a persistent volume under `/data`. The local-versus-hosted storage split described above starts in Phase 7. The delivery model in this ADR is unchanged.

**ADR-0007, new `## Amendments` entry:**

> **<approval date>.** Public mode stays in Phase 4, for operators who run the container on a network or in their own cloud account. The hosted environment template moves to Phase 7 with the DigitalOcean profile ([ADR-0011](ADR-0011-phase4-ships-container-only.md)). Until then, the operator sets `CSFLITE_PUBLIC`, `CSFLITE_PASSWORD` and `CSFLITE_ALLOWED_HOSTS` themselves. Both startup guards still apply.

## Appendix C — Design doc changes (T-4)

| Section | Change |
|---|---|
| §1 | Add: Phase 4 ships the container and the local profile. Network runs are supported, not provisioned. Cite ADR-0011. |
| §3 | Add to non-goals: hosted deployment profiles of any provider, object storage, Postgres. Cite Phase 7. |
| §7 | Database row: SQLite, path in `DATABASE_URL`. Postgres in Phase 7. File storage row: `FileSystemStorage`. Object storage in Phase 7. Rationale paragraph: the seams stay, the second backend arrives in Phase 7. |
| §8 Storage | Filesystem under `CSFLITE_MEDIA_ROOT` only. The object storage sentence moves under a Phase 7 note. The serving rule stays as written. |
| §9 | Remove the `CSFLITE_STORAGE_BACKEND` and `CSFLITE_S3_*` rows and the storage startup guard paragraph. Add one line: these return in Phase 7. `CSFLITE_MEDIA_ROOT` note drops the backend condition. `PORT` note drops the DigitalOcean example. |
| §10 | Replace the DigitalOcean bullet with a network-run bullet: the operator publishes the port, sets `CSFLITE_PUBLIC=true`, `CSFLITE_PASSWORD` and their host in `CSFLITE_ALLOWED_HOSTS`. Both guards apply. |
| §11 | Keep "Local — Phase 4". Add "Network run — operator-deployed, Phase 4": same image, persistent volume at `/data`, public mode, operator provides TLS, temporary-disk hosts unsupported, no template shipped. Replace the DigitalOcean and AWS/Azure/GCP subsections with one "Hosted profiles — Phase 7" subsection holding both. |
| §12 | Remove the `boto3` bullet. |
| §13 | `/login`: "Public mode only (`CSFLITE_PUBLIC=true`)". |
| §17 | Remove the DigitalOcean template, `s3` guard and object storage criteria. Keep both public-mode guards. |
| §18 | Remove the object storage and DigitalOcean risks. Add: network runs need a persistent volume. Add: TLS for network runs is not specified (G-25). |

## Appendix D — `architecture.md` changes (T-7)

- §2 "Talks to": drop the DigitalOcean line. Add network runs (same SQLite and filesystem, on a volume). Later profiles line becomes Phase 7 and includes DigitalOcean.
- §3: Database row becomes SQLite only, Postgres in Phase 7. Driver row (`psycopg`) and File storage row (`django-storages`, `boto3`) marked Phase 7. Auth row: "public mode only" instead of "hosted profile only". Hosting row: container on the operator's machine or host; hosted profiles in Phase 7.
- §4 data stores, TB-1, TB-4, data and secrets rows: drop object storage and S3 keys from Phase 4, or mark them Phase 7.
- AD-4: moved to Phase 7 by ADR-0011. AD-12: "public-mode login", not "hosted login".
- OI-1: mark `django-storages` as Phase 7. OI-10: narrowed. Postgres and Spaces are Phase 7. OI-11: moved to Phase 7. OI-4, OI-5, OI-9: "network run" instead of "hosted".

## Appendix E — `standards.md` and `standards-gaps.md` changes (T-8)

**`standards.md`**
- Scope line: "the local profile and operator-deployed network runs". Drop the DigitalOcean proof of concept.
- CO-17: keep the rule. Drop "Cloud SDKs are reached only through `django-storages`" and replace with a Phase 7 note. Phase 4 ships no cloud SDK.
- INV-14: drop clause (d).
- INV-16: keep the ID. Text becomes "Deferred to Phase 7 with the DigitalOcean template (ADR-0011)".
- INV-17, INV-19, INV-20: scope "public mode" instead of "hosted profile". Rule text unchanged.
- INV-18: drop the two `CSFLITE_S3_*` names.
- F-3: "Deferred to Phase 7 (ADR-0011)".
- §5 environment matrix: replace the DigitalOcean row with "network run (operator-deployed)": one password and a session, reachable as the operator chooses, deploy trigger is the operator's own, data class UNSPECIFIED (G-21). Update the note under the table.

**`standards-gaps.md`**
- G-10: drop the hosted-template wording. The health check problem stays for network runs, where `CSFLITE_ALLOWED_HOSTS` holds only the operator's domain.
- G-17: drop object storage. Mark it Phase 7.
- G-21: reword for network runs.
- arch OI-10 and OI-11 rows: mark moved or narrowed per ADR-0011.
- New G-25, SILENT: TLS for network runs. The password and session cookie cross the network. No source says who terminates TLS or requires HTTPS. Owner: Architect. Affects OI-4, INV-17.
