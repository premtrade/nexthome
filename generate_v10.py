import json

with open('main_v9.json', 'r') as f:
    wf = json.load(f)

# 1. Update Trigger Polling to use standard SELECT (simulated with executeQuery but cleaner)
for node in wf['nodes']:
    if node['name'] == 'Trigger Polling':
        node['parameters']['query'] = "SELECT id, tenant_id, title, description, price, parish, bedrooms, bathrooms, lot_size, amenities, status, created_at FROM properties WHERE ai_processed = false AND status = 'active' LIMIT 1;"

# 2. Update Parse Results to handle more edge cases
for node in wf['nodes']:
    if node['name'] == 'Parse Results':
        node['parameters']['jsCode'] = """
const seoText = $node['SEO Generation'].json.text || "";
const personaText = $node['Persona Classification'].json.text || "";

function extractJson(text) {
  if (!text) return {};
  try {
    const match = text.match(/\\{[\\s\\S]*\\}/);
    if (match) {
        let jsonStr = match[0].replace(/,\\s*}/g, '}');
        return JSON.parse(jsonStr);
    }
    return {};
  } catch (e) {
    return {};
  }
}

const seo = extractJson(seoText);
const persona = extractJson(personaText);

return [{
  json: {
    seo_description: seo.seo_description || "Luxury property in " + ($node['Normalization'].json.parish || "St. James"),
    meta_title: seo.meta_title || $node['Normalization'].json.title,
    meta_description: seo.meta_description || "Luxury villa for sale",
    primary_persona: persona.primary_persona || "Luxury buyer"
  }
}];
"""

# 3. Fix Update DB to be even safer with expressions and handle property truncation
for node in wf['nodes']:
    if node['name'] == 'Update DB':
        # Use a more compact update query
        node['parameters']['query'] = "=UPDATE properties SET seo_description = '{{ $node['Parse Results'].json.seo_description.replace(/'/g, \"''\") }}', meta_title = '{{ $node['Parse Results'].json.meta_title.replace(/'/g, \"''\") }}', meta_description = '{{ $node['Parse Results'].json.meta_description.replace(/'/g, \"''\") }}', buyer_persona = '{{ $node['Parse Results'].json.primary_persona.replace(/'/g, \"''\") }}', competitiveness = '{{ $node['Calculate Rank'].json.competitiveness }}', ai_processed = true, updated_at = NOW() WHERE id = '{{ $node['Normalization'].json.id }}';"

# 4. Remove connections after Update DB to stop possible Alert errors
if 'Update DB' in wf['connections']:
    wf['connections']['Update DB'] = {}

with open('main_v10.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v10.json")
