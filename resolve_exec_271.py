import subprocess
import json
import sys

# Increase recursion depth just in case
sys.setrecursionlimit(2000)

sql = 'SELECT data FROM execution_data WHERE "executionId" = 271;'
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql]
try:
    data_str = subprocess.check_output(cmd).decode('utf-8').strip()
    data = json.loads(data_str)

    visited = {}

    def resolve(v):
        if isinstance(v, str) and v.isdigit():
            idx = int(v)
            if idx in visited:
                return f"<<LOOP: {idx}>>"
            if idx < len(data):
                visited[idx] = True
                res = resolve(data[idx])
                visited[idx] = res
                return res
        if isinstance(v, dict):
            return {k: resolve(val) for k, val in v.items()}
        if isinstance(v, list):
            return [resolve(val) for val in v]
        return v

    resolved = resolve(data[0])
    with open('exec_271_resolved.json', 'w') as f:
        json.dump(resolved, f, indent=2)
    print("Resolved 271.")
except Exception as e:
    print(f"Failed: {e}")
