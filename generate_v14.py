import json

with open('main_v12.json', 'r') as f:
    wf = json.load(f)

# Remove Skip Check node
wf['nodes'] = [n for n in wf['nodes'] if n['name'] != 'Skip Check']

# Remove Skip Check connections
if 'Skip Check' in wf['connections']:
    del wf['connections']['Skip Check']

# Reconnect Normalization directly to SEO Generation
wf['connections']['Normalization'] = {
    "main": [[{"node": "SEO Generation", "type": "main", "index": 0}]]
}

# Update Normalization to return EMPTY array (no items) when nothing to process
# This will naturally stop the workflow chain - n8n won't execute downstream nodes
# if the previous node returned zero items
for node in wf['nodes']:
    if node['name'] == 'Normalization':
        node['parameters']['jsCode'] = """
const items = $input.all();

// If no properties found or empty result, return empty to stop the chain
if (!items || items.length === 0 || !items[0].json || !items[0].json.id) {
  return [];
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
    amenities: Array.isArray(prop.amenities) ? prop.amenities.join(', ') : ''
  }
}];
"""
        print("Updated Normalization node")

with open('main_v14.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v14.json - removed Skip Check, using empty return instead")
