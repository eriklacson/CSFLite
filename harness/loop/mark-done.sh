#!/usr/bin/env bash
# Runs a task's check and writes `done` in the plan's Status column only if it passes.
# Usage: harness/loop/mark-done.sh <stub> <task-id>
# Refuses if the plan or check script changed since approval (<stub>.approved.sha).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec python3 -I harness/loop/planlib.py mark-done "$@"
