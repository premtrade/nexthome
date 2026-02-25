import sqlite3
import json
import os

db_path = 'flowise_db_tmp.sqlite'
# Already copied in previous step, but let's be sure
os.system(f'docker cp next_home_flowise:/root/.flowise/database.sqlite {db_path}')

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Update SEO Generator (3e641813-69b3-4e80-9b6d-51de4e396e58)
cur.execute("SELECT flowData FROM chat_flow WHERE id = '3e641813-69b3-4e80-9b6d-51de4e396e58'")
res = cur.fetchone()
if res:
    flow_json = json.loads(res[0])
    for node in flow_json.get('nodes', []):
        if node['data']['label'] == 'Conversation Chain':
            node['data']['inputs']['systemMessage'] = """You are a real estate SEO expert. Your task is to generate a compelling, SEO-optimized property description, meta title, and meta description based on the provided property details.

Output MUST be a valid JSON object with the following keys:
- seo_description: An engaging description (approx 200-300 words) using keywords naturally.
- meta_title: A punchy meta title under 60 characters.
- meta_description: A concise summary under 160 characters.
"""
        if node['data']['label'] == 'Structured Output Parser':
            node['data']['inputs']['jsonStructure'] = [
                {"property": "seo_description", "type": "string", "description": "SEO optimized description"},
                {"property": "meta_title", "type": "string", "description": "SEO meta title"},
                {"property": "meta_description", "type": "string", "description": "SEO meta description"}
            ]
    
    cur.execute("UPDATE chat_flow SET flowData = ? WHERE id = ?", (json.dumps(flow_json), '3e641813-69b3-4e80-9b6d-51de4e396e58'))

# 2. Update Persona Classifier (734fc77d-ecf1-47eb-bc96-2bab58862c78)
cur.execute("SELECT flowData FROM chat_flow WHERE id = '734fc77d-ecf1-47eb-bc96-2bab58862c78'")
res = cur.fetchone()
if res:
    flow_json = json.loads(res[0])
    for node in flow_json.get('nodes', []):
        if node['data']['label'] == 'Conversation Chain' or node['data']['label'] == 'LLM Chain':
            node['data']['inputs']['systemMessage'] = """You are a real estate market analyst. Classify the property into the most appropriate buyer persona.
Choose ONLY one from: First-time buyer, Luxury buyer, Investor, Diaspora returnee, Commercial investor.
Output MUST be a valid JSON object with keys: primary_persona, confidence."""
        if node['data']['label'] == 'Structured Output Parser':
            node['data']['inputs']['jsonStructure'] = [
                {"property": "primary_persona", "type": "string", "description": "The classified persona"},
                {"property": "confidence", "type": "number", "description": "Confidence score 0-1"}
            ]
    cur.execute("UPDATE chat_flow SET flowData = ? WHERE id = ?", (json.dumps(flow_json), '734fc77d-ecf1-47eb-bc96-2bab58862c78'))

conn.commit()
conn.close()

os.system(f'docker cp {db_path} next_home_flowise:/root/.flowise/database.sqlite')
print("Updated Flowise DB and copied back.")
