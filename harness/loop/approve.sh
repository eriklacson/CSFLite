#!/usr/bin/env bash
# Run by the architect at plan approval, never by the agent.
# Usage: harness/loop/approve.sh <stub>
# Moves harness/drafts/<stub>/ to harness/plans/<stub>/, writes <stub>.approved.sha and sets CURRENT.
# Refuses (exit 4) if the plan's scope_doc is not a file or fails harness/loop/scope-check.sh.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec python3 -I harness/loop/planlib.py approve "$@"
