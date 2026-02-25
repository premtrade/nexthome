import sqlite3
import json
import os

db_path = 'flowise_db_tmp.sqlite'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name, flowData FROM chat_flow WHERE id = '3e641813-69b3-4e80-9b6d-51de4e396e58'")
name, data = cur.fetchone()

print(f"Flow: {name}")
flow_json = json.loads(data)
for node in flow_json.get('nodes', []):
    print(f"Node: {node['data']['label']} ({node['id']})")
    print(f"Inputs: {json.dumps(node['data'].get('inputs', {}), indent=2)}")

conn.close()
