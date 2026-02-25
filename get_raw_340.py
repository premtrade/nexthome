import subprocess
import json

sql = 'SELECT data FROM execution_data WHERE "executionId" = 340;'
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql]

try:
    data = subprocess.check_output(cmd).decode('utf-8').strip()
    with open('exec_340_raw.json', 'w') as f:
        f.write(data)
    print("Saved exec_340_raw.json")
except Exception as e:
    print(f"Error: {e}")
