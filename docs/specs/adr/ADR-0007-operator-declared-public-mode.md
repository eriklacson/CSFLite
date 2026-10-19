# ADR-0007: Require a Password Only When the Operator Declares the Deployment Public

## Status

Accepted

## Date

2026-10-16 ([CHK-0004](../../../.claude/checks/CHK-0004-phase4-container-auth-guard.md))

## Context

An earlier design required a password when the app bound to a non-loopback address. That does not
work in a container. Gunicorn must bind `0.0.0.0` inside the container for Docker's port publishing
to reach it, so the bind address says nothing about who can reach the app.

No other fact visible inside the container tells the app whether it is exposed to a network.

## Decision

The operator declares exposure with `CSFLITE_PUBLIC`.

- **Local** (`CSFLITE_PUBLIC` unset): no login. The shipped compose file publishes the port on
  `127.0.0.1` only.
- **Public** (`CSFLITE_PUBLIC=true`): one operator password from `CSFLITE_PASSWORD`, a Django session,
  no user table.

The app refuses to start when:

1. `CSFLITE_PUBLIC=true` and `CSFLITE_PASSWORD` is unset.
2. `CSFLITE_ALLOWED_HOSTS` is widened beyond `localhost` and `CSFLITE_PUBLIC` is not `true`.

The Railway template ships with `CSFLITE_PUBLIC=true` and the assigned domain in
`CSFLITE_ALLOWED_HOSTS`.

## Consequences

**Positive:**
- A default local run is not reachable from the network.
- Editing only the compose port mapping does not produce an open deployment. Django rejects
  requests whose `Host` is not `localhost`.

**Negative / trade-offs:**
- The control depends on the operator's declaration matching reality. The app cannot detect a
  mismatch.

## Alternatives Considered

**Key the guard off the bind address.** Rejected. It cannot carry the signal inside a container.

**Always require a password.** Rejected. It adds nothing locally, where the real boundary is
Docker's port publishing.

**User accounts and roles.** Rejected. Out of scope for a single operator.
