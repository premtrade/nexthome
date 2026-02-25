import sqlite3
import json

conn = sqlite3.connect('flowise_db_tmp.sqlite')
cur = conn.cursor()
cur.execute("SELECT flowData FROM chat_flow WHERE id = '8a8328f8-352c-4344-8be5-b4dabacb4656'")
row = cur.fetchone()
if row:
    data = json.loads(row[0])
    with open('flowise_nodes_8a8.json', 'w') as f:
        json.dump(data['nodes'], f, indent=2)
    print("Exported flowise_nodes_8a8.json")
else:
    print("Not found")
conn.close()
