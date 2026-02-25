import json

try:
    with open('latest_error_data.json', 'r') as f:
        lines = f.readlines()
        
    # psql output usually has headers and footer
    # Join everything and try to find the JSON start
    content = "".join(lines)
    # Find start of JSON array or object
    start = content.find('[')
    if start == -1:
        start = content.find('{')
    
    end = content.rfind(']')
    if end == -1:
        end = content.rfind('}')
        
    if start != -1 and end != -1:
        json_str = content[start:end+1]
        data = json.loads(json_str)
        
        # execution_data table structure: data column is a JSON
        # It usually contains resultData which has nodes data
        if isinstance(data, list) and len(data) > 0:
            exec_data = data[0].get('data')
            if isinstance(exec_data, str):
                exec_data = json.loads(exec_data)
                
            error = exec_data.get('resultData', {}).get('error', {})
            print("--- Node Failure ---")
            print(f"Node Name: {error.get('nodeName', 'Unknown')}")
            print(f"Message: {error.get('message', 'No message')}")
            print(f"Description: {error.get('description', 'No description')}")
except Exception as e:
    print(f"Failed to parse n8n error data: {e}")
