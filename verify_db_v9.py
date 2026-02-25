import subprocess
import json

sql = "SELECT nodes FROM workflow_entity WHERE id = 'lW5mGPOkiPI7jHXs';"
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql]

try:
    output = subprocess.check_output(cmd).decode('utf-8').strip()
    nodes = json.loads(output)
    for node in nodes:
        if node['name'] == 'Update DB':
            q = node['parameters']['query']
            if "/g" in q:
                print("Found /g in DB")
            else:
                print("NOT Found /g in DB")
            print(f"Query in DB start: {q[:100]}")
except Exception as e:
    print(f"Error: {e}")
