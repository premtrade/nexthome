import json
import subprocess

sql = 'SELECT data FROM execution_data WHERE "executionId" = 31;'
cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-d", "saas_db", "-t", "-A", "-c", sql]

try:
    result = subprocess.check_output(cmd).decode('utf-8')
    # Filter out empty lines or psql noise
    lines = [L for L in result.split('\n') if L.strip()]
    if not lines:
        print("No data found for execution 31.")
    else:
        # psql might return multiple lines if the JSON is pretty-printed or has newlines
        data_str = "".join(lines)
        data = json.loads(data_str)
        
        if isinstance(data, list):
            data = data[0]
            
        # Extract error from resultData
        error = data.get('resultData', {}).get('error', {})
        print("--- Global Error ---")
        print(f"Message: {error.get('message', 'No global error message')}")
        
        # Check node-specific errors
        run_data = data.get('resultData', {}).get('runData', {})
        print("\n--- Node Execution Status ---")
        for node_name, runs in run_data.items():
            for run in runs:
                status = "Error" if 'error' in run else "Success"
                print(f"Node: {node_name} | Status: {status}")
                if 'error' in run:
                    print(f"  Error: {run['error'].get('message')}")

except Exception as e:
    print(f"Error during final debug: {e}")
    # Also print the raw result if it failed to parse
    try:
        print(f"Raw result (first 100 chars): {result[:100]}")
    except:
        pass
