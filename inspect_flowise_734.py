import sqlite3
import json

conn = sqlite3.connect('flowise_db_tmp.sqlite')
cur = conn.cursor()
cur.execute("SELECT flowData FROM chat_flow WHERE id = '734fc77d-ecf1-47eb-bc96-2bab58862c78'")
row = cur.fetchone()
if row:
    data = json.loads(row[0])
    with open('flowise_nodes_734.json', 'w') as f:
        json.dump(data['nodes'], f, indent=2)
    print("Exported flowise_nodes_734.json")
else:
    print("Not found")
conn.close()
