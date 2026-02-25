import json

# Load the working JSON
with open('main_workflow_fixed.json', 'r') as f:
    wf = json.load(f)

# Update node 3 (SEO Generation) parameters
for node in wf['nodes']:
    if node['name'] == 'SEO Generation':
        node['parameters']['jsonBody'] = "={\n  \"question\": \"Generate SEO for this property:\\nTitle: {{ $json.title }}\\nLocation: {{ $json.parish }}\\nBedrooms: {{ $json.bedrooms }}\\nBathrooms: {{ $json.bathrooms }}\\nPrice: {{ $json.price }}\\nAmenities: {{ $json.amenities_text }}\",\n  \"overrideConfig\": {\n    \"property_id\": \"{{ $json.id }}\",\n    \"tenant_id\": \"{{ $json.tenant_id }}\"\n  }\n}"

with open('main_v4.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v4.json")
