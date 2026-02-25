import subprocess

sql = 'SELECT "versionId", "activeVersionId" FROM workflow_entity WHERE id = \'lW5mGPOkiPI7jHXs\';'
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-c", sql]
print(subprocess.check_output(cmd).decode('utf-8'))
