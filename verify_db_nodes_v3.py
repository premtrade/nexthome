import subprocess
import json

workflow_id = 'lW5mGPOkiPI7jHXs'
sql = f"SELECT nodes FROM workflow_entity WHERE id = '{workflow_id}';"
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql]

try:
    output = subprocess.check_output(cmd).decode('utf-8').strip()
    nodes = json.loads(output)
    print(f"Workflow ID: {workflow_id}")
    for node in nodes:
        if node['name'] in ['SEO Generation', 'Persona Classification']:
            print(f"\nNode: {node['name']}")
            print(f"JSON Body: {node['parameters'].get('jsonBody')}")
except Exception as e:
    print(f"Error: {e}")
