import json
import subprocess

def get_error(exec_id):
    print(f"\n--- Checking Execution {exec_id} ---")
    sql_data = f'SELECT data FROM execution_data WHERE "executionId" = {exec_id};'
    cmd_data = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql_data]
    try:
        data_str = subprocess.check_output(cmd_data).decode('utf-8').strip()
        data = json.loads(data_str)
        
        def resolve(v):
            if isinstance(v, str) and v.isdigit():
                idx = int(v)
                if idx < len(data):
                    return resolve(data[idx])
            return v

        meta = data[0]
        result_data = resolve(meta.get('resultData'))
        
        if isinstance(result_data, dict):
            error = resolve(result_data.get('error'))
            if isinstance(error, dict):
                print(f"Global Error: {resolve(error.get('message'))}")
                # print(f"Description: {resolve(error.get('description'))}")
            
            run_data = resolve(result_data.get('runData'))
            if isinstance(run_data, dict):
                for node_name, runs_ref in run_data.items():
                    runs = resolve(runs_ref)
                    if isinstance(runs, list):
                        for run_ref in runs:
                            run = resolve(run_ref)
                            if isinstance(run, dict) and run.get('error'):
                                err = resolve(run.get('error'))
                                print(f"Node '{node_name}' Error: {resolve(err.get('message'))}")
    except Exception as e:
        print(f"Failed to parse {exec_id}: {e}")

# Get last few execs
sql_list = 'SELECT id FROM execution_entity ORDER BY id DESC LIMIT 10;'
cmd_list = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql_list]
try:
    ids = subprocess.check_output(cmd_list).decode('utf-8').strip().split('\n')
    for eid in ids:
        if eid:
            get_error(int(eid))
except Exception as e:
    print(f"List failed: {e}")
