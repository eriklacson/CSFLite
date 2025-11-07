from pathlib import Path


def test_convert_and_write_csv(tmp_path: Path) -> None:
    from tools import nuclei_json_converter
    from tools.global_helpers import write_to_csv

    raw_entries = [
        {
            "template-id": "tpl-1",
            "host": "https://example.com",
            "matched-at": "https://example.com",
            "timestamp": "2024-01-01T00:00:00Z",
            "info": {
                "severity": "medium",
                "description": "Example finding",
                "name": "example-matcher",
            },
        }
    ]

    csv_path = tmp_path / "results" / "scan.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    normalized = nuclei_json_converter.convert_nuclei_raw(raw_entries)
    write_to_csv(normalized, csv_path)

    written = csv_path.read_text(encoding="utf-8").splitlines()

    assert written[0].split(",") == [
        "templateID",
        "host",
        "matched-at",
        "severity",
        "timestamp",
        "matcher-name",
        "description",
    ]
    assert "tpl-1" in written[1]
