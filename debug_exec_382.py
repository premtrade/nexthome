import subprocess
import json
import sys

sys.setrecursionlimit(2000)

# Get the latest execution data
sql = 'SELECT data FROM execution_data WHERE "executionId" = 382;'
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
    
    # Print Trigger Polling and Normalization data
    rd = resolved.get('resultData', {}).get('runData', {})
    
    if 'Trigger Polling' in rd:
        tp = rd['Trigger Polling']
        if isinstance(tp, list) and len(tp) > 0:
            tp_data = tp[0].get('data', {}).get('main', [[]])[0]
            print(f"Trigger Polling returned {len(tp_data)} items")
            if tp_data:
                print(f"  First item keys: {list(tp_data[0].get('json', {}).keys())}")
    
    if 'Normalization' in rd:
        norm = rd['Normalization']
        if isinstance(norm, list) and len(norm) > 0:
            norm_data = norm[0].get('data', {}).get('main', [[]])[0]
            print(f"Normalization returned {len(norm_data)} items")
            if norm_data:
                print(f"  First item: {json.dumps(norm_data[0].get('json', {}), indent=2)[:500]}")
    
    if 'Skip Check' in rd:
        sc = rd['Skip Check']
        if isinstance(sc, list) and len(sc) > 0:
            print(f"Skip Check executed, status: {sc[0].get('executionStatus')}")
            sc_data = sc[0].get('data', {}).get('main', [[], []])
            print(f"  True path items: {len(sc_data[0]) if len(sc_data) > 0 else 0}")
            print(f"  False path items: {len(sc_data[1]) if len(sc_data) > 1 else 0}")

except Exception as e:
    print(f"Failed: {e}")
