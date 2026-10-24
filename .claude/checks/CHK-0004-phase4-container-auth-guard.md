# CHK-0004: Phase 4 Container Auth Guard

## Date

2026-10-16

## Scope

`docs/specs/design/phase-4-web-interface.md` §9–§12, specifically the startup guard that was meant to
prevent an unauthenticated assessment tool from being reachable on a network.

Prompted by the design review ahead of Phase 4 build-out, continuing from CHK-0003.

## Findings

| # | Status | Finding |
|---|---|---|
| 1 | Fixed | Auth guard keyed off a bind address that cannot carry that signal inside a container |
| 2 | Fixed | Residual risk from finding 1 — editing only the compose port mapping had no guard at all |

---

## 1. Auth guard keyed off a bind address that cannot carry that signal inside a container

**Status:** Fixed

**Location:** §9 (`CSFLITE_BIND`), §10 (Authentication), §12 (Container)

§10 said: bind to `127.0.0.1` and no login is required; bind elsewhere and `CSFLITE_PASSWORD` is
required, enforced by a startup guard. §12 said the container is the only artifact, including the
local profile.

Docker's published ports reach a container through its own network namespace, not through
`127.0.0.1` — a process that binds only `127.0.0.1` inside the container is unreachable even from
the host, regardless of any `-p`/`ports:` mapping. Gunicorn has to bind `0.0.0.0` inside the
container for `docker compose up` to work at all, in every profile, local included. Since the
address the application can observe is always `0.0.0.0`, the guard as specified would have
required a password for every deployment, local or hosted — directly contradicting §10's "Local:
none," or the guard would need to be skipped for the local profile, defeating its purpose for the
one profile that forgets to set a password most easily.

**Reproduction:** none needed — this is a property of how Docker's NAT-based port publishing
works, not a code path. Any container process that binds `127.0.0.1` is unreachable from outside
its own network namespace; `docker compose up` with the design's stated default
(`CSFLITE_BIND=127.0.0.1:8000`) would not serve the local profile at all.

**Why it matters.** The guard exists to stop organisation assessment data from being exposed
unauthenticated. A guard that cannot distinguish local from hosted either fails open (never
trips, so a forgotten password on a public host goes unnoticed) or fails the one profile it
wasn't meant to restrict (local). Either failure mode defeats the control silently — no one
discovers it until something is actually exposed or a user can't reach `docker compose up` on
their own laptop.

**Resolution.** The application can't observe network reachability from inside a container, so
authentication stops being inferred from anything the process can see. `CSFLITE_BIND` is removed.
Gunicorn always binds `0.0.0.0:$PORT` (§12). A new operator-declared flag, `CSFLITE_PUBLIC`
(default `false`), replaces the bind-address check; the startup guard now fails when
`CSFLITE_PUBLIC=true` and `CSFLITE_PASSWORD` is unset (§10).

The actual network boundary moves to the deployment profile, which can enforce it where the
application cannot (§11):

- Local: the shipped `docker-compose.yml` publishes `127.0.0.1:${PORT:-8000}:8000`, not
  `0.0.0.0:8000:8000`. `CSFLITE_PUBLIC` stays unset.
- Railway: no loopback-only option exists on that platform, so the shipped environment template
  sets `CSFLITE_PUBLIC=true` by default — a fresh deploy with no password fails at boot.

Residual risk, recorded rather than solved: an operator who edits the local compose file's port
mapping to `0.0.0.0` without also setting `CSFLITE_PUBLIC` is not caught by anything the
application can check. Logged in §18 Open risks.

No application code exists yet to change — this is a design-doc fix, closing the gap before the
Django view and `docker-compose.yml` get written.

---

## 2. Residual risk from finding 1 — editing only the compose port mapping had no guard at all

**Status:** Fixed

**Location:** §9 (`CSFLITE_ALLOWED_HOSTS`), §10 (Authentication), §18 (Open risks)

Finding 1's resolution left one case genuinely unguarded: an operator edits the local compose
file's port mapping from `127.0.0.1:8000:8000` to `0.0.0.0:8000:8000` and changes nothing else.
`CSFLITE_PUBLIC` stays `false`. Nothing the application does catches this, because — as finding 1
established — the application cannot observe which address the port is published on from inside
the container.

**Why it matters.** This was recorded as an accepted residual risk, not a real guard. An edit to
one line of a compose file, with no corresponding change anywhere the application could check,
was enough to make a deployment holding organisation assessment data reachable from the operator's
network with no password.

**Resolution.** `CSFLITE_ALLOWED_HOSTS` was already specified (default `localhost`) but its role
as a security control had not been drawn out — it was documented as an ordinary Django setting.
Django rejects any request whose `Host` header is not in `ALLOWED_HOSTS` with a 400, before the
request reaches a view, independent of which address the port is published on. With the default
held, editing only the port mapping does not produce a working deployment: a LAN or public
request arrives with that address as its `Host` header, not `localhost`, and is rejected.

Making such a deployment actually functional requires widening `CSFLITE_ALLOWED_HOSTS` — the one
step the application *can* observe, because it's reading its own configuration, not inspecting
the network. A new startup guard added to §10 ties that widening to the existing one:
`CSFLITE_ALLOWED_HOSTS` set beyond its default while `CSFLITE_PUBLIC` is not `true` now also
fails to start. The two declarations — host allowlist and password requirement — can no longer
drift apart.

This does not make the port-mapping edit detectable. It makes the edit, by itself, insufficient —
the gap closes because the request that would prove the deployment is exposed is the same request
Django already refuses by default, not because the application learned to see the port mapping.
§18's risk row is updated accordingly rather than removed, since the port mapping edit itself is
still invisible to the application.
