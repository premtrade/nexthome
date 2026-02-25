import json

with open('main_v8.json', 'r') as f:
    wf = json.load(f)

for node in wf['nodes']:
    if node['name'] == 'Update DB':
        # Use global regex for escaping single quotes
        node['parameters']['query'] = "=UPDATE properties SET seo_description = '{{ $node['Parse Results'].json.seo_description.replace(/'/g, \"''\") }}', meta_title = '{{ $node['Parse Results'].json.meta_title.replace(/'/g, \"''\") }}', meta_description = '{{ $node['Parse Results'].json.meta_description.replace(/'/g, \"''\") }}', buyer_persona = '{{ $node['Parse Results'].json.primary_persona.replace(/'/g, \"''\") }}', competitiveness = '{{ $node['Calculate Rank'].json.competitiveness }}', ai_processed = true, updated_at = NOW() WHERE id = '{{ $node['Normalization'].json.id }}' AND tenant_id = '{{ $node['Normalization'].json.tenant_id }}';"

with open('main_v9.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v9.json")
