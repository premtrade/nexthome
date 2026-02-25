import subprocess
import json
import sys

sys.setrecursionlimit(2000)

for exec_id in [362, 363, 365]:
    sql = f'SELECT data FROM execution_data WHERE "executionId" = {exec_id};'
    cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql]
    try:
        data_str = subprocess.check_output(cmd).decode('utf-8').strip()
        if not data_str:
            print(f"Exec {exec_id}: No data yet")
            continue
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
        err = resolved.get('resultData', {}).get('error', {})
        if isinstance(err, dict):
            msg = err.get('message', 'unknown')
            node_name = err.get('node', {})
            if isinstance(node_name, dict):
                node_name = node_name.get('name', 'unknown')
            print(f"Exec {exec_id}: Error at '{node_name}' -> {msg}")
        else:
            print(f"Exec {exec_id}: No structured error")
    except Exception as e:
        print(f"Exec {exec_id}: Failed: {e}")
