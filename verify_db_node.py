import subprocess
import json

sql = "SELECT nodes::text FROM workflow_entity WHERE id = 'lW5mGPOkiPI7jHXs';"
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql]
output = subprocess.check_output(cmd).decode('utf-8')
nodes = json.loads(output)

for node in nodes:
    if node['name'] == 'SEO Generation':
        print(f"JSON Body for SEO Generation:\n{node['parameters'].get('jsonBody')}")
