# CHK-0004: Phase 4 Container Auth Guard

## Date

2026-10-16

## Scope

`docs/design/phase-4-web-interface.md` §9–§12, specifically the startup guard that was meant to
prevent an unauthenticated assessment tool from being reachable on a network.

Prompted by the design review ahead of Phase 4 build-out, continuing from CHK-0003.

## Findings

| # | Status | Finding |
|---|---|---|
| 1 | Fixed | Auth guard keyed off a bind address that cannot carry that signal inside a container |

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

**Why it matters.** The guard exists to stop client assessment data from being exposed
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
