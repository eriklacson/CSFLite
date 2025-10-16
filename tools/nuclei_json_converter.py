"""Utilities for normalizing Nuclei scan JSON output."""

import json  # noqa: F401
from pathlib import Path  # noqa: F401
from typing import Any, Dict, List, Mapping, Sequence, Union


def normalize_raw_entries(raw: Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Normalize the raw JSON structure into a list of dictionaries.

    Handle Nuclei scan results as either a sequence (``[{}, {}, ...]``) or as
    newline-delimited JSON objects.
    """

    if isinstance(raw, Mapping):
        return [dict(raw)]

    if isinstance(raw, Sequence):
        entries: List[Dict[str, Any]] = []
        for item in raw:
            if not isinstance(item, Mapping):
                raise TypeError("Each entry in the raw Nuclei data must be a mapping/dict.")
            entries.append(dict(item))
        return entries

    raise TypeError("Raw Nuclei data must be a mapping or a sequence of mappings.")
