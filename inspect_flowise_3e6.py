import sqlite3
import json

conn = sqlite3.connect('flowise_db_tmp.sqlite')
cur = conn.cursor()
cur.execute("SELECT flowData FROM chat_flow WHERE id = '3e641813-69b3-4e80-9b6d-51de4e396e58'")
row = cur.fetchone()
if row:
    data = json.loads(row[0])
    with open('flowise_nodes_3e6.json', 'w') as f:
        json.dump(data['nodes'], f, indent=2)
    print("Exported flowise_nodes_3e6.json")
else:
    print("Not found")
conn.close()
