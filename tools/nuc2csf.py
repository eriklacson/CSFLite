import json
import csv

input_file = 'nuclei_output.json'
output_file = 'findings.csv'

fields = ['timestamp', 'host', 'template_id', 'severity', 'matcher_name', 'description', 'matched_url']

with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fields)
    writer.writeheader()
    
    for line in infile:
        try:
            entry = json.loads(line)
            writer.writerow({
                'timestamp': entry.get('timestamp'),
                'host': entry.get('host'),
                'template_id': entry.get('templateID'),
                'severity': entry.get('info', {}).get('severity'),
                'matcher_name': entry.get('matcher_name', ''),
                'description': entry.get('info', {}).get('name'),
                'matched_url': entry.get('matched', ''),
            })
        except json.JSONDecodeError:
            continue
