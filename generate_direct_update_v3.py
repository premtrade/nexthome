import json
import uuid

def get_sql(file_path, workflow_id, new_name=None):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    if new_name:
        data['name'] = new_name
        
    # Generate a new version ID
    new_version_id = str(uuid.uuid4())
    
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
    name = '{new_name or data['name']}',
    "versionId" = '{new_version_id}',
    "activeVersionId" = '{new_version_id}',
    active = true
WHERE id = '{workflow_id}';
"""
    return sql

with open('update_direct_v3.sql', 'w') as f:
    f.write(get_sql('main_workflow_fixed.json', 'lW5mGPOkiPI7jHXs', "Next Home - Property AI Processor V3"))
    f.write(get_sql('error_workflow.json', 'rqxDLuVBtw4fTaEw'))

print("Generated update_direct_v3.sql")
