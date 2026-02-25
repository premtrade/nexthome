import json

def get_sql(file_path, workflow_id):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Extract nodes, connections, settings
    nodes = json.dumps(data['nodes'])
    connections = json.dumps(data['connections'])
    settings = json.dumps(data.get('settings', {}))
    
    # Escape single quotes
    nodes_esc = nodes.replace("'", "''")
    connections_esc = connections.replace("'", "''")
    settings_esc = settings.replace("'", "''")
    
    sql = f"""
UPDATE workflow_entity 
SET nodes = '{nodes_esc}', 
    connections = '{connections_esc}', 
    settings = '{settings_esc}',
    active = true
WHERE id = '{workflow_id}';
"""
    return sql

with open('update_direct.sql', 'w') as f:
    f.write(get_sql('main_workflow_fixed.json', 'lW5mGPOkiPI7jHXs'))
    f.write(get_sql('error_workflow.json', 'rqxDLuVBtw4fTaEw'))

print("Generated update_direct.sql")
