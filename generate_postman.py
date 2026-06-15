import json
import os

items = []

for file in os.listdir('json_output'):
    if file.endswith('.json'):
        with open(f'json_output/{file}', 'r') as f:
            alert_data = json.load(f)

        alert_name = file.replace('.json', '')
        items.append({
            "name": f"Create-{alert_name}",
            "request": {
                "method": "POST",
                "header": [
                    {"key": "Content-Type", "value": "application/json"},
                    {"key": "Authorization", "value": "Basic YWRtaW46T3BzdHJlZUAxMjM="},
                    {"key": "X-Disable-Provenance", "value": "true"}
                ],
                "url": {
                    "raw": "https://grafana.opstree.net/api/v1/provisioning/alert-rules",
                    "protocol": "https",
                    "host": ["grafana", "opstree", "net"],
                    "path": ["api", "v1", "provisioning", "alert-rules"]
                },
                "body": {
                    "mode": "raw",
                    "raw": json.dumps(alert_data, indent=2),
                    "options": {"raw": {"language": "json"}}
                }
            }
        })

postman_collection = {
    "info": {
        "name": "Grafana-Alert-Rules-POC",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": items
}

with open('postman_collection.json', 'w') as f:
    json.dump(postman_collection, f, indent=2)

print(f"Postman Collection ready with {len(items)} alerts!")
