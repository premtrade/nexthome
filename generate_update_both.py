import json

def get_sql(file_path, workflow_id):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    nodes = json.dumps(data['nodes'])
    connections = json.dumps(data['connections'])
    settings = json.dumps(data['settings'])
    
    # Escape single quotes for SQL
    sql = f"""
UPDATE workflow_entity 
SET nodes = '{nodes.replace("'", "''")}', 
    connections = '{connections.replace("'", "''")}', 
    settings = '{settings.replace("'", "''")}',
    active = true
WHERE id = '{workflow_id}';
"""
    return sql

sql_main = get_sql('main_workflow_fixed.json', 'lW5mGPOkiPI7jHXs')
sql_error = get_sql('error_workflow.json', 'rqxDLuVBtw4fTaEw')

with open('update_both.sql', 'w') as f:
    f.write(sql_main)
    f.write(sql_error)

print("Generated update_both.sql")
