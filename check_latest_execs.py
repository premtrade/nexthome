import subprocess

sql = 'SELECT id, "workflowId", status, "startedAt" FROM execution_entity ORDER BY "startedAt" DESC LIMIT 10;'
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-c", sql]
print(subprocess.check_output(cmd).decode('utf-8'))
