import subprocess
import json

sql = "SELECT id, nodes::text FROM workflow_entity WHERE id = 'lW5mGPOkiPI7jHXs';"
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql]
output = subprocess.check_output(cmd).decode('utf-8')
id_val, nodes_str = output.split('|', 1)
nodes = json.loads(nodes_str)

print(f"Workflow ID: {id_val}")
for node in nodes:
    if node['name'] == 'SEO Generation':
        print(f"JSON Body for SEO Generation:\n{node['parameters'].get('jsonBody')}")
