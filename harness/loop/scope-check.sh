#!/usr/bin/env bash
# Checks that a scope file follows docs/scopes/template.scope.md.
# Usage: harness/loop/scope-check.sh <file> | --all
# Exit 0 pass, 1 fail, 2 usage error.
set -euo pipefail
if [ "$#" -ne 1 ]; then
  echo "usage: scope-check.sh <file> | --all" >&2
  exit 2
fi
arg="$1"
# Resolve a relative path before moving to the repo root, so the script works from any folder.
if [ "$arg" != "--all" ] && [ "${arg#/}" = "$arg" ]; then
  arg="$PWD/$arg"
fi
cd "$(git rev-parse --show-toplevel)"
exec python3 -I harness/loop/planlib.py scope-check "$arg"
