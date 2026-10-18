# ADR-0006: Ship a Self-Hosted Container, Portable but Not Elastic

## Status

Accepted

## Date

2026-08-30

## Context

CSFLite processes client assessment data. That data should not leave an environment the operator
controls. The CLI met this by running only on the operator's machine.

A web app needs a delivery model that keeps that property.

## Decision

**Delivery.** CSFLite ships a container image. The operator runs it on their own machine or in their
own cloud account. CSFLite is never offered as a hosted service.

**One artifact.** The container is the only artifact, including for local use. Local runs use
`docker compose up`. Railway is the first hosted profile. AWS, Azure, and GCP come later.

**Portable, not elastic.** Config comes from the environment, logs go to stdout, and there is no
provider-specific code. The app runs always-on with one worker. It does not scale to zero or
autoscale. pandas adds about a second of import time to every cold start, and one operator creates
no load.

## Consequences

**Positive:**
- Client data stays in the operator's environment. This resolves the local-first constraint.
- Running locally exercises the same path as a hosted deployment.

**Negative / trade-offs:**
- Docker is required on the assessor's machine.
- The image is about 100 MB larger because of pandas and numpy.

## Alternatives Considered

**Hosted SaaS.** Rejected. CSFLite would hold client data.

**Serverless or scale-to-zero.** Rejected. Cold starts pay the pandas import on every request.
Recorded so a later change does not "fix" the app into a serverless deployment.

**Local Python install as a second path.** Rejected. Two sets of instructions and two artifacts.
