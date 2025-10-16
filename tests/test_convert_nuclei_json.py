"""Tests for the Nuclei raw JSON converter utilities."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is available *before* any site-packages "tools" module.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
