import json

with open('main_v10.json', 'r') as f:
    wf = json.load(f)

# Fix Check Alerts node to reference Parse Results instead of Persona Classification
for node in wf['nodes']:
    if node['name'] == 'Check Alerts':
        node['parameters']['conditions']['conditions'] = [
            {
                "leftValue": "={{ $node['Calculate Rank'].json.competitiveness }}",
                "rightValue": "Underpriced",
                "operator": {
                    "type": "string",
                    "operation": "equals"
                }
            },
            {
                "leftValue": "={{ $node['Parse Results'].json.primary_persona }}",
                "rightValue": "Investor",
                "operator": {
                    "type": "string",
                    "operation": "equals"
                }
            }
        ]
        # Also ensure options are set correctly
        node['parameters']['options'] = {}
        print(f"Fixed Check Alerts node")

# Ensure connection from Update DB -> Check Alerts exists
wf['connections']['Update DB'] = {
    "main": [[{"node": "Check Alerts", "type": "main", "index": 0}]]
}

with open('main_v11.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v11.json")
