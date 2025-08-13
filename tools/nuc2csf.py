import json
import csv

input_file = "../scans/sample_output.json"
output_file = "../output/findings.csv"

fields = [
    "template_id",
    "host",
    "matched_at",
    "severity",
    "timestamp",
    "matcher_name",
    "description",
]

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fields)
    writer.writeheader()

    for line in infile:
        try:
            entry = json.loads(line)
            writer.writerow(
                {
                    "timestamp": entry.get("timestamp"),
                    "host": entry.get("host"),
                    "template_id": entry.get("templateID"),
                    "severity": entry.get("info", {}).get("severity"),
                    "matcher_name": entry.get("matcher_name", ""),
                    "description": entry.get("info", {}).get("name"),
                    "matched_url": entry.get("matched", ""),
                }
            )
        except json.JSONDecodeError:
            continue
