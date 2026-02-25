import sqlite3
import json
import os

db_path = 'flowise_db_tmp.sqlite'
# Copy DB from container
os.system(f'docker cp next_home_flowise:/root/.flowise/database.sqlite {db_path}')

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT id, name, flowData FROM chat_flow")
flows = cur.fetchall()

for fid, name, data in flows:
    print(f"--- Flow: {name} ({fid}) ---")
    try:
        flow_json = json.loads(data)
        # Find prompts
        for node in flow_json.get('nodes', []):
            if 'prompt' in node.get('data', {}).get('inputs', {}):
                print(f"Node: {node['id']} ({node['data']['label']})")
                print(f"Prompt: {node['data']['inputs']['prompt']}")
            if 'systemMessage' in node.get('data', {}).get('inputs', {}):
                print(f"Node: {node['id']} ({node['data']['label']})")
                print(f"System Message: {node['data']['inputs']['systemMessage']}")
    except Exception as e:
        print(f"Error parsing flow data: {e}")

conn.close()
