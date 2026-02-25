import subprocess

sql = 'SELECT id, name, "versionId", "activeVersionId", active FROM workflow_entity;'
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-c", sql]
print(subprocess.check_output(cmd).decode('utf-8'))
