import json

# Load the working JSON
with open('main_workflow_fixed.json', 'r') as f:
    wf = json.load(f)

def fix_expressions(obj):
    if isinstance(obj, str):
        # Replace $node[\"Normalization\"] or $node["Normalization"] with $node['Normalization']
        import re
        # First handle the escaped version we saw
        obj = obj.replace(r'$node[\"Normalization\"]', "$node['Normalization']")
        obj = obj.replace(r'$node[\"SEO Generation\"]', "$node['SEO Generation']")
        obj = obj.replace(r'$node[\"Persona Classification\"]', "$node['Persona Classification']")
        obj = obj.replace(r'$node[\"Calculate Rank\"]', "$node['Calculate Rank']")
        # Also handle non-escaped if any
        obj = obj.replace(r'$node["Normalization"]', "$node['Normalization']")
        obj = obj.replace(r'$node["SEO Generation"]', "$node['SEO Generation']")
        obj = obj.replace(r'$node["Persona Classification"]', "$node['Persona Classification']")
        obj = obj.replace(r'$node["Calculate Rank"]', "$node['Calculate Rank']")
        return obj
    if isinstance(obj, dict):
        return {k: fix_expressions(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [fix_expressions(v) for v in obj]
    return obj

wf = fix_expressions(wf)

# Also ensure node 3 and 4 have the NEW format
for node in wf['nodes']:
    if node['name'] == 'SEO Generation':
        node['parameters']['jsonBody'] = "={\n  \"question\": \"Generate SEO for this property:\\nTitle: {{ $json.title }}\\nLocation: {{ $json.parish }}\\nBedrooms: {{ $json.bedrooms }}\\nBathrooms: {{ $json.bathrooms }}\\nPrice: {{ $json.price }}\\nAmenities: {{ $json.amenities_text }}\",\n  \"overrideConfig\": {\n    \"property_id\": \"{{ $json.id }}\",\n    \"tenant_id\": \"{{ $json.tenant_id }}\"\n  }\n}"
    if node['name'] == 'Persona Classification':
        node['parameters']['jsonBody'] = "={\n  \"question\": \"Classify persona for this property:\\nTitle: {{ $node['Normalization'].json.title }}\\nDescription: {{ $node['Normalization'].json.description }}\\nPrice: {{ $node['Normalization'].json.price }}\\nAmenities: {{ $node['Normalization'].json.amenities_text }}\",\n  \"overrideConfig\": {\n    \"property_id\": \"{{ $node['Normalization'].json.id }}\",\n    \"tenant_id\": \"{{ $node['Normalization'].json.tenant_id }}\"\n  }\n}"
    if node['name'] == 'Gen Embeddings':
        node['parameters']['jsonBody'] = "={\n  \"question\": \"generate embeddings\",\n  \"input\": \"Title: {{ $node['Normalization'].json.title }}\\nLocation: {{ $node['Normalization'].json.parish }}\\nBedrooms: {{ $node['Normalization'].json.bedrooms }}\\nPrice: {{ $node['Normalization'].json.price }}\\nSEO Description: {{ $node['SEO Generation'].json.seo_description }}\\nAmenities: {{ $node['Normalization'].json.amenities_text }}\\nPersona: {{ $node['Persona Classification'].json.primary_persona }}\",\n  \"overrideConfig\": {\n    \"property_id\": \"{{ $node['Normalization'].json.id }}\",\n    \"tenant_id\": \"{{ $node['Normalization'].json.tenant_id }}\"\n  }\n}"

with open('main_v5.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v5.json")
