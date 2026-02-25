import json

with open('main_v6.json', 'r') as f:
    wf = json.load(f)

# 1. Add Parse Results node
parse_node = {
    "parameters": {
        "jsCode": "const seoText = $node['SEO Generation'].json.text;\nconst personaText = $node['Persona Classification'].json.text;\n\nfunction extractJson(text) {\n  if (!text) return {};\n  try {\n    const match = text.match(/\\{[\\s\\S]*\\}/);\n    if (match) return JSON.parse(match[0]);\n    return {};\n  } catch (e) {\n    return {};\n  }\n}\n\nconst seo = extractJson(seoText);\nconst persona = extractJson(personaText);\n\nreturn [{\n  json: {\n    seo_description: seo.seo_description || \"\",\n    meta_title: seo.meta_title || \"\",\n    meta_description: seo.meta_description || \"\",\n    primary_persona: persona.primary_persona || \"Investor\"\n  }\n}];"
    },
    "id": "parse_results_id",
    "name": "Parse Results",
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [1000, 100]
}

wf['nodes'].append(parse_node)

# 2. Re-route connections
# Persona Classification -> Parse Results -> Get Competitor Prices
if 'Persona Classification' in wf['connections']:
    old_targets = wf['connections']['Persona Classification'].get('main', [[]])[0]
    wf['connections']['Persona Classification']['main'] = [[{"node": "Parse Results", "type": "main", "index": 0}]]
    wf['connections']['Parse Results'] = {"main": [old_targets]}
else:
    # Error if not found, but it should be there
    print("Warning: Persona Classification connection not found")

# 3. Update nodes that use Persona/SEO output
for node in wf['nodes']:
    if node['name'] == 'Gen Embeddings':
        node['parameters']['jsonBody'] = "={\n  \"question\": \"generate embeddings\",\n  \"input\": \"Title: {{ $node['Normalization'].json.title }}\\nLocation: {{ $node['Normalization'].json.parish }}\\nBedrooms: {{ $node['Normalization'].json.bedrooms }}\\nPrice: {{ $node['Normalization'].json.price }}\\nSEO Description: {{ $node['Parse Results'].json.seo_description }}\\nAmenities: {{ $node['Normalization'].json.amenities_text }}\\nPersona: {{ $node['Parse Results'].json.primary_persona }}\",\n  \"overrideConfig\": {\n    \"property_id\": \"{{ $node['Normalization'].json.id }}\",\n    \"tenant_id\": \"{{ $node['Normalization'].json.tenant_id }}\"\n  }\n}"
    
    if node['name'] == 'Update DB':
        # Use query expression for robustness
        node['parameters']['query'] = "=UPDATE properties SET seo_description = '{{ $node['Parse Results'].json.seo_description.replace(\"'\", \"''\") }}', meta_title = '{{ $node['Parse Results'].json.meta_title.replace(\"'\", \"''\") }}', meta_description = '{{ $node['Parse Results'].json.meta_description.replace(\"'\", \"''\") }}', buyer_persona = '{{ $node['Parse Results'].json.primary_persona.replace(\"'\", \"''\") }}', competitiveness = '{{ $node['Calculate Rank'].json.competitiveness }}', ai_processed = true, updated_at = NOW() WHERE id = '{{ $node['Normalization'].json.id }}' AND tenant_id = '{{ $node['Normalization'].json.tenant_id }}';"
        if 'queryParams' in node['parameters']:
            del node['parameters']['queryParams']

with open('main_v7.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v7.json")
