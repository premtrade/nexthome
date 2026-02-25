import sqlite3

conn = sqlite3.connect('flowise_db_tmp.sqlite')
cur = conn.cursor()
cur.execute("SELECT id, name, credentialName FROM credential")
rows = cur.fetchall()
for r in rows:
    print(f"ID: {r[0]}, Name: {r[1]}, Type: {r[2]}")
conn.close()
