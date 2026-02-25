import sqlite3
import json

conn = sqlite3.connect('flowise_db_tmp.sqlite')
cur = conn.cursor()
cur.execute("SELECT id, name FROM chat_flow")
rows = cur.fetchall()
for r in rows:
    print(f"ID: {r[0]}, Name: {r[1]}")
conn.close()
