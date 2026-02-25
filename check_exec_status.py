import subprocess

sql = 'SELECT id, status, "startedAt" FROM execution_entity WHERE "workflowId" = \'lW5mGPOkiPI7jHXs\' ORDER BY "startedAt" DESC LIMIT 20;'
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-c", sql]

try:
    print(subprocess.check_output(cmd).decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
