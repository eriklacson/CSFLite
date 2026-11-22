#!/usr/bin/env bash
# Run by the architect at plan approval, never by the agent.
# Usage: harness/loop/approve.sh <stub>
# Moves harness/drafts/<stub>/ to harness/plans/<stub>/, writes <stub>.approved.sha and sets CURRENT.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec python3 -I harness/loop/planlib.py approve "$@"
