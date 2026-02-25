import subprocess

sql = 'SELECT "versionId", "createdAt" FROM workflow_history WHERE "workflowId" = \'lW5mGPOkiPI7jHXs\' ORDER BY "createdAt" DESC LIMIT 5;'
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-c", sql]
print(subprocess.check_output(cmd).decode('utf-8'))
