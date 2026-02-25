import sqlite3
import json

conn = sqlite3.connect('flowise_db_tmp.sqlite')
cur = conn.cursor()
cur.execute("SELECT id, name, flowData FROM chat_flow")
rows = cur.fetchall()
for id, name, flowData in rows:
    if "qdrant" in flowData.lower():
        print(f"Found Qdrant in flow: {name} (ID: {id})")
conn.close()
