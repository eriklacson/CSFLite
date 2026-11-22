---
plan: phase4-descope
scope_doc: docs/specs/phase-4/web-interface-scope.md
status: approved
round_limit: 3
---

# Plan phase4-descope — Cut Phase 4 to the container; move hosted profiles to Phase 7

> Approved by the architect on 2026-11-22. Only the Status column may change from here, and only through `mark-done.sh`.

## What this plan delivers

The Phase 4 records describe one container image, run locally or on a network the operator controls. Every hosted profile moves to Phase 7.

## The change in plain words

**Stays in Phase 4**

- The Django app: questionnaire, evidence upload, report, heatmap, CSV export, CSV import.
- One container image. The local `docker compose` profile, published on `127.0.0.1`.
- Public mode (ADR-0007): `CSFLITE_PUBLIC`, `CSFLITE_PASSWORD`, `/login`, both startup guards.
- Network runs. An operator may run the container on a network or in their own cloud account. CSFLite supports this but ships no template or provisioning for it.
- HTTPS in public mode. The operator's proxy or load balancer provides TLS. The app requires HTTPS: it redirects HTTP, sends cookies only over HTTPS, and sends HSTS. The local profile is unchanged and runs over plain HTTP.
- SQLite and evidence files on disk, under `/data`. A network run needs `/data` on a persistent volume. Later releases add provisions for hosts without one.
- The SQLite file sits at a fixed path, `/data/csflite.db`. No setting is needed for it.
- Environment variables are added only where an operator needs to change a value.
- CLI retirement and the golden parity gate.

**Moves to Phase 7**

- The DigitalOcean proof of concept: App Platform, Managed Postgres, Spaces, its environment template.
- Object storage: `django-storages`, `boto3`, `CSFLITE_STORAGE_BACKEND`, the `CSFLITE_S3_*` settings, the storage startup guard.
- Postgres, `psycopg` and `DATABASE_URL`.
- AWS, Azure and GCP (already Phase 7).

**Phase numbers and names do not change.** Phase 5 stays Release Hardening. Phase 6 stays Community. Phase 7 stays Multi-Cloud Deployment Profiles and gains the DigitalOcean proof of concept. Its start condition is not recorded in this repository.

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

The "cut rule" in the checks: a line that names a moved item (DigitalOcean, App Platform, Spaces, Managed Postgres, `CSFLITE_S3_*`, `CSFLITE_STORAGE_BACKEND`, `django-storages`, `boto3`, `psycopg`, `DATABASE_URL`) must say `Phase 7` or `ADR-0011`, or sit under a heading that does.

| ID | Task | Depends on | Check | Round limit | Status |
|---|---|---|---|---|---|
| T-1 | Write ADR-0011 from the text in Appendix A, status Accepted, dated the approval day. Add it to the ADR index. | — | `bash harness/plans/phase4-descope/phase4-descope.check.sh T-1` | 3 | done |
| T-2 | Add a dated amendment to ADR-0006 and ADR-0007 that points to ADR-0011 (Appendix B). Add text only. Delete nothing. | T-1 | `bash harness/plans/phase4-descope/phase4-descope.check.sh T-2` | 3 | done |
| T-3 | Scope doc: remove the DigitalOcean profile from "In scope". Add network runs. Add the moved items to "Out of scope" under Phase 7. Drop the DigitalOcean acceptance line. Cite ADR-0011. | T-1 | `bash harness/plans/phase4-descope/phase4-descope.check.sh T-3` | 3 | done |
| T-4 | Design doc, per Appendix C: §1, §3, §7, §8, §9, §10, §11, §12, §13, §17, §18. | T-1 | `bash harness/plans/phase4-descope/phase4-descope.check.sh T-4` | 3 | done |
| T-5 | Spec brief: §7 Phase 4 paragraph, the §10 "Container is the only artifact" row, §12 delivery paragraph. Cite ADR-0011. | T-1 | `bash harness/plans/phase4-descope/phase4-descope.check.sh T-5` | 3 | done |
| T-6 | Roadmap: Phase 4 deliverables and acceptance criteria lose the DigitalOcean and storage items and gain network runs. Phase 7 keeps its name and gains the DigitalOcean proof of concept, object storage and Postgres. No start condition is written. | T-1 | `bash harness/plans/phase4-descope/phase4-descope.check.sh T-6` | 3 | done |
| T-7 | `architecture.md`, per Appendix D. | T-1 | `bash harness/plans/phase4-descope/phase4-descope.check.sh T-7` | 3 | done |
| T-8 | `standards.md` and `standards-gaps.md`, per Appendix E. Add rule INV-30 (HTTPS in public mode). Add G-25 as resolved by it. | T-1 | `bash harness/plans/phase4-descope/phase4-descope.check.sh T-8` | 3 | done |
| T-9 | Confirm only the files listed above changed in `docs/`, and the cut rule holds across `docs/` outside ADRs and checks. | T-2 to T-8 | `bash harness/plans/phase4-descope/phase4-descope.check.sh T-9` | 3 | todo |

## How the tasks cover the scope

No scope doc exists in `docs/scopes/` for this change. It changes the Phase 4 scope summary itself. Rule P-9 needs an accepted decision record for a scope change. ADR-0011 is that record.

| Criterion | Task |
|---|---|
| The scope change has an accepted decision record (P-9) | T-1, T-2 |
| Phase 4 records name no hosted profile, object storage or Postgres, except as Phase 7 | T-3 to T-8 |
| Public mode and network runs stay in Phase 4 | T-3, T-4, T-8 |
| Public mode requires HTTPS; local mode does not | T-1, T-4, T-8 |
| Phase 7 holds every hosted profile | T-6 |
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
- **Phase 7 timing.** Decided outside this repository. No changed file names it. T-9 checks that no changed file names the commercial product.

## Decisions taken (architect, 2026-11-22)

1. **Phase 7 start condition.** Not recorded in this repository. Phase 7 keeps its name.
2. **`DATABASE_URL`.** Removed from Phase 4. The SQLite path is fixed. Environment variables are added only as needed.
3. **Persistent volume.** Accepted as a Phase 4 risk. Later releases add provisions for it.
4. **TLS.** Option A. The operator terminates TLS in front of the container. In public mode the app requires HTTPS. No escape hatch: public mode over plain HTTP is not supported. No new setting.

## Open items for the architect

1. **Approve the ADR-0011 text** in Appendix A.
2. **HSTS details (proposed).** One year (`max-age=31536000`). No `includeSubDomains` and no `preload`, because the operator's other subdomains are not CSFLite's to lock to HTTPS. Approve or change.
3. **`/healthz` and the redirect (proposed).** The container health check calls `/healthz` over plain HTTP from inside the container. A redirect would make it fail. The plan exempts `/healthz` from the HTTPS redirect only. The other `/healthz` problem in G-10 (the `Host` header) stays open.
4. **Same pattern, not changed here.** `CSFLITE_MEDIA_ROOT` and `CSFLITE_CSF_LOOKUP` are also paths that operators rarely change. This plan leaves them alone. Say if they should go the same way as `DATABASE_URL`.

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

**Public mode requires HTTPS.** The operator terminates TLS in a proxy or load balancer in front
of the container. With `CSFLITE_PUBLIC=true` the app redirects HTTP to HTTPS, marks the session
and CSRF cookies `Secure`, sends HSTS, and reads the proxy's `X-Forwarded-Proto` header to know
the request arrived over HTTPS. `/healthz` is exempt from the redirect only. No new setting:
public mode turns this on. With `CSFLITE_PUBLIC` unset, none of it applies and the local profile
runs over plain HTTP on `127.0.0.1`.

**Storage is SQLite and the filesystem.** Both live under `/data`. The SQLite file is at the
fixed path `/data/csflite.db`. A network run needs `/data` on a persistent volume.

**Environment variables only where needed.** Phase 4 adds a variable only when an operator needs
to change the value. `DATABASE_URL` is not one of them. It returns with Postgres in Phase 7.

**Hosted profiles move to Phase 7.** Phase 7 keeps its name. It gains the DigitalOcean proof of
concept, object storage and Postgres, beside the AWS, Azure and GCP profiles it already holds.
Its start condition is not recorded in this repository.

The portability rules do not change. Configuration comes from the environment. Application code
does not call a provider API or branch on the provider.

## Consequences

**Positive:**
- Phase 4 is smaller. No `boto3`, `django-storages` or `psycopg`. No `DATABASE_URL` parser. No
  storage guard. No template.
- The `django-storages` support risk leaves Phase 4.
- No cloud cost before there is a user.

**Negative / trade-offs:**
- The object storage path is not tested until Phase 7.
- A network run depends on a persistent volume. A host with only temporary disk loses data.
  Such hosts are unsupported in Phase 4. Later releases add provisions for them.
- Moving to Postgres in Phase 7 adds a setting and a data migration path from SQLite.
- Public mode over plain HTTP does not work. Browsers do not send `Secure` cookies over HTTP, so
  login fails. This includes an office network with no certificate.
- A network run needs a TLS proxy in front of the container. The app trusts that proxy's
  `X-Forwarded-Proto` header. Exposed directly, a client could fake the header and skip the
  redirect. Cookies still stay off plain HTTP. The documentation says a proxy is required.
- Operators who run on a network get documentation, not a template.

## Alternatives Considered

**Keep the DigitalOcean proof of concept in Phase 4.** Rejected. No user justifies the cost.

**Loopback-only Phase 4, with public mode deferred.** Rejected. Operators can usefully run the
container on a network or in their own cloud account now.

**Make cloud Phase 5 and renumber.** Rejected. "Phase 5" for the supplements is written into
ADR-0008, the design, the spec brief, `architecture.md` and `AGENTS.md`.

**Keep `DATABASE_URL` as the SQLite path setting.** Rejected. Nobody needs to change the path in
Phase 4, and it would need a parser (architecture OI-12).

**Ship a TLS proxy (such as Caddy) in the compose file.** Rejected. It adds a shipped component
and amounts to the network-run template this ADR leaves out.

**Gunicorn serves TLS with operator certificates.** Rejected. It adds two settings and leaves
certificate renewal to the operator by hand.

**An escape hatch for public mode over plain HTTP.** Rejected. It adds a setting and sends the
password unencrypted.

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
| §7 | Database row: SQLite at the fixed path `/data/csflite.db`. Postgres and `DATABASE_URL` in Phase 7. File storage row: `FileSystemStorage`. Object storage in Phase 7. Rationale paragraph: the seams stay, the second backend arrives in Phase 7. |
| §8 Storage | Filesystem under `CSFLITE_MEDIA_ROOT` only. The object storage sentence moves under a Phase 7 note. The serving rule stays as written. |
| §9 | Remove the `DATABASE_URL`, `CSFLITE_STORAGE_BACKEND` and `CSFLITE_S3_*` rows and the storage startup guard paragraph. Add one line: these return in Phase 7. State the fixed SQLite path. `CSFLITE_MEDIA_ROOT` note drops the backend condition. `PORT` note drops the DigitalOcean example. |
| §10 | Replace the DigitalOcean bullet with a network-run bullet: the operator publishes the port, puts a TLS proxy in front, sets `CSFLITE_PUBLIC=true`, `CSFLITE_PASSWORD` and their host in `CSFLITE_ALLOWED_HOSTS`. Both guards apply. Add an "HTTPS in public mode" paragraph: redirect, `Secure` cookies, HSTS, `X-Forwarded-Proto`, `/healthz` redirect exemption. Local mode: none of these. |
| §11 | Keep "Local — Phase 4". Add "Network run — operator-deployed, Phase 4": same image, persistent volume at `/data`, public mode, a TLS proxy in front (required), temporary-disk hosts unsupported until later releases, no template shipped. Replace the DigitalOcean and AWS/Azure/GCP subsections with one "Hosted profiles — Phase 7" subsection holding both. |
| §12 | Remove the `boto3` bullet. |
| §13 | `/login`: "Public mode only (`CSFLITE_PUBLIC=true`)". |
| §17 | Remove the DigitalOcean template, `s3` guard and object storage criteria. Keep both public-mode guards. Add: with `CSFLITE_PUBLIC=true`, an HTTP request is redirected to HTTPS, cookies are `Secure`, and responses carry HSTS. With it unset, none of these apply. `/healthz` is not redirected. |
| §18 | Remove the object storage and DigitalOcean risks. Add: network runs need a persistent volume; accepted for Phase 4, later releases add provisions. Add: public mode over plain HTTP fails login; accepted. Add: exposing the container without a proxy lets a client fake `X-Forwarded-Proto`; the docs require a proxy. |

## Appendix D — `architecture.md` changes (T-7)

- §2 "Talks to": drop the DigitalOcean line. Add network runs (same SQLite and filesystem, on a volume). Later profiles line becomes Phase 7 and includes DigitalOcean.
- §3: Database row becomes SQLite only, at a fixed path. Postgres and `DATABASE_URL` in Phase 7. Driver row (`psycopg`) and File storage row (`django-storages`, `boto3`) marked Phase 7. Auth row: "public mode only" instead of "hosted profile only". Hosting row: container on the operator's machine or host; hosted profiles in Phase 7.
- §4 data stores, TB-1, TB-4, data and secrets rows: drop object storage, S3 keys and `DATABASE_URL` from Phase 4, or mark them Phase 7.
- AD-4: moved to Phase 7 by ADR-0011. AD-12: "public-mode login", not "hosted login".
- OI-1: mark `django-storages` as Phase 7. OI-10: narrowed. Postgres and Spaces are Phase 7. OI-11 and OI-12: moved to Phase 7. OI-4: `Secure` decided by INV-30; `HttpOnly`, `SameSite` and session lifetime stay open. OI-5, OI-9: "network run" instead of "hosted".

## Appendix E — `standards.md` and `standards-gaps.md` changes (T-8)

**`standards.md`**
- Scope line: "the local profile and operator-deployed network runs". Drop the DigitalOcean proof of concept.
- CO-17: keep the rule. Drop "Cloud SDKs are reached only through `django-storages`" and replace with a Phase 7 note. Phase 4 ships no cloud SDK.
- INV-14: drop clause (d).
- INV-16: keep the ID. Text becomes "Deferred to Phase 7 with the DigitalOcean template (ADR-0011)".
- INV-17, INV-19, INV-20: scope "public mode" instead of "hosted profile". Rule text unchanged.
- New INV-30 (approved 2026-11-22, ADR-0011): with `CSFLITE_PUBLIC=true` the app **MUST** redirect HTTP to HTTPS (except `/healthz`), mark session and CSRF cookies `Secure`, send HSTS, and treat a request as HTTPS only from `X-Forwarded-Proto: https`. With `CSFLITE_PUBLIC` unset, none of these apply. Mechanism proposed: settings tests in both modes and a redirect test.
- INV-18: drop the two `CSFLITE_S3_*` names and `DATABASE_URL`.
- CO-8: `PORT` is the only exception to the `CSFLITE_` prefix in Phase 4. `DATABASE_URL` returns as an exception in Phase 7.
- F-3: "Deferred to Phase 7 (ADR-0011)".
- §5 environment matrix: replace the DigitalOcean row with "network run (operator-deployed)": one password and a session, reachable as the operator chooses, deploy trigger is the operator's own, data class UNSPECIFIED (G-21). Update the note under the table.

**`standards-gaps.md`**
- G-10: drop the hosted-template wording. The health check problem stays for network runs, where `CSFLITE_ALLOWED_HOSTS` holds only the operator's domain.
- G-17: drop object storage. Mark it Phase 7.
- G-21: reword for network runs.
- arch OI-10, OI-11 and OI-12 rows: mark moved or narrowed per ADR-0011.
- New G-25, SILENT: TLS for network runs. The password and session cookie cross the network. RESOLVED 2026-11-22 by ADR-0011 and INV-30: the operator terminates TLS, the app requires HTTPS in public mode. Affects OI-4, INV-17, INV-30.
