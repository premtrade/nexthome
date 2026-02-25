import json
import subprocess

sql = 'SELECT id, "workflowId", status, "startedAt" FROM execution_entity WHERE status = \'error\' ORDER BY "startedAt" DESC LIMIT 1;'
# Use -c with double quotes around the whole thing, and escape internal quotes
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-c", sql]

try:
    result = subprocess.check_output(cmd).decode('utf-8')
    print("--- Latest Error ---")
    print(result)

    # Parse result
    lines = [L.strip() for L in result.split('\n') if L.strip() and not L.startswith('-')]
    if len(lines) >= 2:
        parts = lines[1].split('|')
        if len(parts) >= 1:
            exec_id = parts[0].strip()
            print(f"Latest Execution ID: {exec_id}")
            
            sql_data = f'SELECT data FROM execution_data WHERE "executionId" = {exec_id};'
            cmd_data = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-c", sql_data]
            data_result = subprocess.check_output(cmd_data).decode('utf-8')
            with open('latest_error_data.json', 'w') as f:
                f.write(data_result)
            print(f"Detailed error data dumped to latest_error_data.json")
except Exception as e:
    print(f"Error: {e}")
