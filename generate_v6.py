import json

# Load the working JSON
with open('main_v5.json', 'r') as f:
    wf = json.load(f)

for node in wf['nodes']:
    if node['name'] == 'Get Competitor Prices':
        # Use query expression instead of separate parameters
        node['parameters']['query'] = "=SELECT price FROM properties WHERE parish = '{{ $node['Normalization'].json.parish }}' AND bedrooms = {{ $node['Normalization'].json.bedrooms }} AND status = 'active' AND tenant_id = '{{ $node['Normalization'].json.tenant_id }}' LIMIT 50;"
        if 'queryParams' in node['parameters']:
            del node['parameters']['queryParams']

with open('main_v6.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v6.json")
