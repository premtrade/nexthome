import json

with open('main_v7.json', 'r') as f:
    wf = json.load(f)

# 1. Bypass Gen Embeddings
# Calculate Rank -> Update DB
if 'Calculate Rank' in wf['connections']:
    wf['connections']['Calculate Rank']['main'] = [[{"node": "Update DB", "type": "main", "index": 0}]]

# 2. Fix Parse Results node (ensure it handles empty strings and has a proper ID)
for node in wf['nodes']:
    if node['name'] == 'Parse Results':
        node['parameters']['jsCode'] = """
const seoText = $node['SEO Generation'].json.text;
const personaText = $node['Persona Classification'].json.text;

function extractJson(text) {
  if (!text) return {};
  try {
    const match = text.match(/\\{[\\s\\S]*\\}/);
    if (match) {
        // Remove trailing commas which AI often includes and JSON.parse hates
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
    seo_description: seo.seo_description || "",
    meta_title: seo.meta_title || "",
    meta_description: seo.meta_description || "",
    primary_persona: persona.primary_persona || "Investor"
  }
}];
"""

with open('main_v8.json', 'w') as f:
    json.dump(wf, f, indent=2)

print("Created main_v8.json")
