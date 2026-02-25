import json

with open('main_v12.json', 'r') as f:
    wf = json.load(f)

# Fix the Skip Check node - use a simpler string comparison
for node in wf['nodes']:
    if node['name'] == 'Skip Check':
        node['parameters'] = {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeCondition": "string"
                },
                "conditions": [
                    {
                        "id": "skip-condition",
                        "leftValue": "={{ $json.skip }}",
                        "rightValue": "false",
                        "operator": {
                            "type": "string",
                            "operation": "equals"
                        }
                    }
                ],
                "combinator": "and"
            },
            "options": {}
        }
        print("Fixed Skip Check node")

with open('main_v13.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v13.json")
