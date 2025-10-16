"""Utilities for normalizing Nuclei scan JSON output.

This module exposes helpers to convert the verbose JSON emitted by
Nuclei scans into the simplified structure consumed by CSFLite.  The
simplified structure mirrors the example stored in
``scans/sample_output.json``.

Why the seemingly elaborate normalisation helpers?
    The raw JSON produced by Nuclei is not consistently shaped.  A scan
    can emit a single object or a stream/array of objects depending on
    how it was invoked, and individual entries may omit or rename
    fields (``host`` vs ``url``) across versions of the tool.  Rather
    than forcing each caller to re-implement brittle conditionals, the
    converter centralises the heuristics for

    * accepting both singleton objects and arrays,
    * keeping the output resilient to missing optional fields, and
    * cleaning up free-form text so that reports render nicely.

    The helpers therefore look a little more involved than a naïve
    field mapping, but in practice they keep the calling code and tests
    straightforward because the edge-cases are handled in one place.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Union


def _coerce_to_entries(raw: Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]) -> List[Dict[str, Any]]:
    """Normalize the raw JSON structure into a list of dictionaries.

    Nuclei can emit scan results as a sequence (``[{}, {}, ...]``) or as
    newline-delimited JSON objects that some callers pre-load one at a
    time.  Accepting both forms means we can feed in data as it was read
    without forcing extra wrapping logic.
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


def _clean_text(value: Any) -> str:
    """Return a human-friendly string representation for JSON fields."""

    if value is None:
        return ""

    if isinstance(value, str):
        # Collapse internal whitespace so multi-line descriptions read well.
        return " ".join(value.split())

    return str(value)


def _convert_entry(entry: Mapping[str, Any]) -> Dict[str, str]:
    """Convert a single Nuclei JSON object into CSFLite's summary format.

    Field names in the raw payload have changed between historical
    versions of Nuclei (``template-id``/``templateID`` and
    ``host``/``url`` are the most common examples).  Pulling everything
    through a helper ensures we keep a single, well documented set of
    fallbacks instead of scattering ``dict.get`` chains across the app.
    """

    info = entry.get("info")
    if isinstance(info, Mapping):
        severity = info.get("severity")
        description = info.get("description") or info.get("name")
        fallback_matcher = info.get("name")
    else:
        severity = None
        description = None
        fallback_matcher = None

    matcher_name = entry.get("matcher-name") or fallback_matcher

    result = {
        "templateID": _clean_text(entry.get("template-id") or entry.get("templateID")),
        "host": _clean_text(entry.get("host") or entry.get("url") or entry.get("matched-at")),
        "matched-at": _clean_text(entry.get("matched-at") or entry.get("url")),
        "severity": _clean_text(severity),
        "timestamp": _clean_text(entry.get("timestamp")),
        "matcher-name": _clean_text(matcher_name),
        "description": _clean_text(description),
    }

    return result


def convert_nuclei_raw(raw_data: Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]) -> List[Dict[str, str]]:
    """Convert in-memory Nuclei JSON data into the simplified summary format."""

    entries = _coerce_to_entries(raw_data)
    return [_convert_entry(item) for item in entries]


def convert_nuclei_raw_file(path: Union[str, Path]) -> List[Dict[str, str]]:
    """Load a raw Nuclei JSON file and convert it to the summary format.

    Parameters
    ----------
    path:
        Path to a JSON file produced by Nuclei.  The file may contain a
        single JSON object or a JSON array of objects.
    """

    json_path = Path(path)
    with json_path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    return convert_nuclei_raw(raw)
