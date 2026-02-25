import json
import subprocess

def get_node_data(exec_id, target_node):
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
            run_data = resolve(result_data.get('runData'))
            if isinstance(run_data, dict) and target_node in run_data:
                node_runs = resolve(run_data[target_node])
                for run_ref in node_runs:
                    run = resolve(run_ref)
                    print(f"\n--- Node: {target_node} (Exec: {exec_id}) ---")
                    # Check Input
                    input_data = resolve(run.get('data', {}).get('main', [[]])[0][0])
                    print(f"Input Data Snippet: {json.dumps(input_data, indent=2)[:500]}")
                    
                    # Check Output / Error
                    if run.get('error'):
                        print(f"Error: {resolve(run.get('error'))}")
    except Exception as e:
        print(f"Failed: {e}")

get_node_data(132, "SEO Generation")
get_node_data(132, "Normalization")
