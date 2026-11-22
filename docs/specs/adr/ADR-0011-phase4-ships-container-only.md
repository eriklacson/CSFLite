# ADR-0011: Phase 4 Ships the Container Only; Hosted Profiles Move to Phase 7

## Status

Accepted

## Date

2026-11-22

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
