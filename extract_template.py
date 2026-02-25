import sqlite3
import json
import os

db_path = 'flowise_db_tmp.sqlite'
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name, flowData FROM chat_flow WHERE id = '3e641813-69b3-4e80-9b6d-51de4e396e58'")
name, data = cur.fetchone()

flow_json = json.loads(data)
for node in flow_json.get('nodes', []):
    if node['data']['label'] == 'Conversation Chain':
        print(f"Template:\n{node['data'].get('inputs', {}).get('template')}")

conn.close()
