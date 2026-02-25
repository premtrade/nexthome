import json
import subprocess

sql = 'SELECT data FROM execution_data ORDER BY "executionId" DESC LIMIT 1;'
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql]

try:
    result = subprocess.check_output(cmd).decode('utf-8').strip()
    # n8n database result for 'data' column is a JSON array
    data_list = json.loads(result)
    
    # In n8n execution_data, 'data' column usually looks like:
    # [{"version":1,"startData":"...","resultData":"...","executionData":"..."}, {}, {...}]
    # The actual execution details are often in resultData as a stringified JSON
    for item in data_list:
        if isinstance(item, dict) and 'resultData' in item:
            # resultData might be stringified JSON
            rd = item['resultData']
            if isinstance(rd, str):
                rd = json.loads(rd)
            
            error = rd.get('error')
            if error:
                print(f"--- Global Error ---")
                print(f"Message: {error.get('message')}")
            
            run_data = rd.get('runData', {})
            for node_name, runs in run_data.items():
                for run in runs:
                    if run.get('error'):
                        print(f"\n--- Node: {node_name} ---")
                        print(f"Error: {run['error'].get('message')}")
                        print(f"Details: {run['error'].get('description')}")

except Exception as e:
    print(f"Extraction failed: {e}")
    if 'result' in locals():
        print(f"Raw Snippet: {result[:200]}")
