import subprocess

sql = 'SELECT id, "workflowId", "workflowVersionId" FROM execution_entity WHERE id = 257;'
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql]
print(subprocess.check_output(cmd).decode('utf-8'))
