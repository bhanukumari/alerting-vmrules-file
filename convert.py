import yaml
import json
import os

input_dir = 'alerting_file'
output_dir = 'json_output'

FOLDER_UID = "bfol2pegi35dsd"
ORG_ID = 2
DATASOURCE_UID = "victoriametrics"

os.makedirs(output_dir, exist_ok=True)

def convert_expr(expr):
    return " ".join(line.strip() for line in expr.strip().splitlines())

def build_grafana_json(rule):
    return {
        "title": rule.get("alert", "unknown"),
        "ruleGroup": "kubernetes-apps-poc",
        "folderUID": FOLDER_UID,
        "noDataState": "OK",
        "execErrState": "OK",
        "for": rule.get("for", "5m") or "5m",
        "orgID": ORG_ID,
        "uid": "",
        "condition": "B",
        "annotations": rule.get("annotations", {}),
        "labels": rule.get("labels", {}),
        "data": [
            {
                "refId": "A",
                "queryType": "",
                "relativeTimeRange": {"from": 600, "to": 0},
                "datasourceUid": DATASOURCE_UID,
                "model": {
                    "expr": convert_expr(rule.get("expr", "")),
                    "hide": False,
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "refId": "A"
                }
            },
            {
                "refId": "B",
                "queryType": "",
                "relativeTimeRange": {"from": 0, "to": 0},
                "datasourceUid": "-100",
                "model": {
                    "conditions": [
                        {
                            "evaluator": {"params": [0], "type": "gt"},
                            "operator": {"type": "and"},
                            "query": {"params": ["A"]},
                            "reducer": {"params": [], "type": "last"},
                            "type": "query"
                        }
                    ],
                    "datasource": {"type": "__expr__", "uid": "-100"},
                    "hide": False,
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "refId": "B",
                    "type": "classic_conditions"
                }
            }
        ]
    }

def build_create_request(alert_name, grafana_json):
    return {
        "name": f"Create-{alert_name}",
        "event": [
            {
                "listen": "test",
                "script": {
                    "exec": [
                        f"var jsonData = pm.response.json();",
                        f"if (jsonData.uid) {{",
                        f"    pm.environment.set('UID_{alert_name}', jsonData.uid);",
                        f"    console.log('UID saved: ' + jsonData.uid);",
                        f"}}"
                    ],
                    "type": "text/javascript"
                }
            }
        ],
        "request": {
            "method": "POST",
            "header": [
                {"key": "Content-Type", "value": "application/json"},
                {"key": "Authorization", "value": "Bearer {{TOKEN}}"},
                {"key": "X-Disable-Provenance", "value": "true"}
            ],
            "url": {
                "raw": "{{BASE_URL}}/api/v1/provisioning/alert-rules",
                "host": ["{{BASE_URL}}"],
                "path": ["api", "v1", "provisioning", "alert-rules"]
            },
            "body": {
                "mode": "raw",
                "raw": json.dumps(grafana_json, indent=2),
                "options": {"raw": {"language": "json"}}
            }
        }
    }

def build_get_request(alert_name):
    return {
        "name": f"Get-{alert_name}",
        "event": [
            {
                "listen": "test",
                "script": {
                    "exec": [
                        f"var jsonData = pm.response.json();",
                        f"var alert = jsonData.find(a => a.title === '{alert_name}');",
                        f"if (alert) {{",
                        f"    pm.environment.set('UID_{alert_name}', alert.uid);",
                        f"    console.log('UID found: ' + alert.uid);",
                        f"}} else {{",
                        f"    console.log('Alert {alert_name} not found');",
                        f"}}"
                    ],
                    "type": "text/javascript"
                }
            }
        ],
        "request": {
            "method": "GET",
            "header": [
                {"key": "Authorization", "value": "Bearer {{TOKEN}}"},
                {"key": "X-Disable-Provenance", "value": "true"}
            ],
            "url": {
                "raw": "{{BASE_URL}}/api/v1/provisioning/alert-rules",
                "host": ["{{BASE_URL}}"],
                "path": ["api", "v1", "provisioning", "alert-rules"]
            }
        }
    }

def build_delete_request(alert_name):
    return {
        "name": f"Delete-{alert_name}",
        "request": {
            "method": "DELETE",
            "header": [
                {"key": "Authorization", "value": "Bearer {{TOKEN}}"},
                {"key": "X-Disable-Provenance", "value": "true"}
            ],
            "url": {
                "raw": "{{BASE_URL}}/api/v1/provisioning/alert-rules/{{UID_" + alert_name + "}}",
                "host": ["{{BASE_URL}}"],
                "path": ["api", "v1", "provisioning", "alert-rules", "{{UID_" + alert_name + "}}"]
            }
        }
    }

# Postman collection structure
postman_collection = {
    "info": {
        "name": "Grafana-Alert-Rules-POC",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": []
}

for file in os.listdir(input_dir):
    if file.endswith('.yaml') or file.endswith('.yml'):
        with open(f'{input_dir}/{file}', 'r') as f:
            data = yaml.safe_load(f)

        rules = data['spec']['groups'][0]['rules']
        print(f"Processing {file} - Found {len(rules)} rules")

        for rule in rules:
            alert_name = rule.get('alert', 'unknown')
            grafana_json = build_grafana_json(rule)

            # Individual JSON file save karo
            json_file = f"{output_dir}/{alert_name}.json"
            with open(json_file, 'w') as f:
                json.dump(grafana_json, f, indent=2)
            print(f"  Converted: {alert_name} → {json_file}")

            # Teenon requests add karo
            postman_collection["item"].append(build_create_request(alert_name, grafana_json))
            postman_collection["item"].append(build_get_request(alert_name))
            postman_collection["item"].append(build_delete_request(alert_name))

# Postman collection save karo
with open("postman_collection.json", "w") as f:
    json.dump(postman_collection, f, indent=2)
print("Postman collection saved: postman_collection.json")

print("Done!")