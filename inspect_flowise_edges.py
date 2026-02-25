import sqlite3
import json
import os

db_path = 'flowise_db_tmp.sqlite'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT flowData FROM chat_flow WHERE id = '3e641813-69b3-4e80-9b6d-51de4e396e58'")
data = cur.fetchone()[0]

flow_json = json.loads(data)
print("--- Edges ---")
for edge in flow_json.get('edges', []):
    print(f"{edge['source']} -> {edge['target']}")

for node in flow_json.get('nodes', []):
    if node['type'] == 'customNode':
        print(f"Node: {node['id']} ({node['data']['label']})")
        if 'chatPromptTemplate' in node['data'].get('inputs', {}):
             print(f"  Connected Template: {node['data']['inputs']['chatPromptTemplate']}")

conn.close()
