import sqlite3
import json

conn = sqlite3.connect('flowise_db_tmp.sqlite')
cur = conn.cursor()
cur.execute("SELECT name, flowData FROM chat_flow WHERE id = '8a8328f8-352c-4344-8be5-b4dabacb4656'")
row = cur.fetchone()
if row:
    name, flowData = row
    data = json.loads(flowData)
    print(f"Flow Name: {name}")
    print(f"Node types: {[n['data']['name'] for n in data['nodes']]}")
    # Save the whole flowData to inspect edges
    with open('flowise_flow_8a8.json', 'w') as f:
        json.dump(data, f, indent=2)
else:
    print("Not found")
conn.close()
