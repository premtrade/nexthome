import json

with open('main_v11.json', 'r') as f:
    wf = json.load(f)

# Update the Normalization node to check for empty results and stop if none
for node in wf['nodes']:
    if node['name'] == 'Normalization':
        node['parameters']['jsCode'] = """
const items = $input.all();

// If no properties found, return early with a flag
if (!items || items.length === 0 || !items[0].json || !items[0].json.id) {
  return [{ json: { skip: true } }];
}

const prop = items[0].json;
return [{
  json: {
    id: prop.id || '',
    tenant_id: prop.tenant_id || '',
    title: prop.title || '',
    description: prop.description || '',
    price: prop.price || '0',
    parish: prop.parish || '',
    bedrooms: prop.bedrooms || 0,
    bathrooms: prop.bathrooms || 0,
    amenities: Array.isArray(prop.amenities) ? prop.amenities.join(', ') : '',
    skip: false
  }
}];
"""

# Add an IF node right after Normalization to check for skip flag
# Find if we already have a "Skip Check" node
skip_check_exists = any(n['name'] == 'Skip Check' for n in wf['nodes'])
if not skip_check_exists:
    skip_check_node = {
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeCondition": "string"
                },
                "conditions": [
                    {
                        "leftValue": "={{ $json.skip }}",
                        "rightValue": "={{ false }}",
                        "operator": {
                            "type": "boolean",
                            "operation": "equals"
                        }
                    }
                ],
                "combinator": "and"
            },
            "options": {}
        },
        "id": "skip-check-id",
        "name": "Skip Check",
        "type": "n8n-nodes-base.if",
        "typeVersion": 2,
        "position": [550, 300]
    }
    wf['nodes'].append(skip_check_node)

    # Rewire: Normalization -> Skip Check -> SEO Generation (true path)
    # Instead of: Normalization -> SEO Generation
    wf['connections']['Normalization'] = {
        "main": [[{"node": "Skip Check", "type": "main", "index": 0}]]
    }
    wf['connections']['Skip Check'] = {
        "main": [
            [{"node": "SEO Generation", "type": "main", "index": 0}],  # true path
            []  # false path (skip - do nothing)
        ]
    }

with open('main_v12.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v12.json with skip-check guard")
