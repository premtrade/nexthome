import json
import subprocess

# Correct Credential ID
CRED_ID = "UiVjly5vgM3yn3AG"
CRED_NAME = "Postgres account"

# Correct Error Workflow ID
ERROR_WF_ID = "rqxDLuVBtw4fTaEw"

with open('main_workflow.json', 'r') as f:
    data = json.load(f)

# Update all postgres nodes in the JSON data
for node in data['nodes']:
    if node['type'] == 'n8n-nodes-base.postgres':
        node['credentials']['postgres']['id'] = CRED_ID
        node['credentials']['postgres']['name'] = CRED_NAME

# Update settings with correct Error Workflow ID
data['settings']['errorWorkflow'] = ERROR_WF_ID

nodes = json.dumps(data['nodes'])
connections = json.dumps(data['connections'])
settings = json.dumps(data['settings'])

sql = f"""
UPDATE workflow_entity 
SET nodes = '{nodes.replace("'", "''")}', 
    connections = '{connections.replace("'", "''")}', 
    settings = '{settings.replace("'", "''")}',
    active = true
WHERE id = 'lW5mGPOkiPI7jHXs';
"""

with open('update_workflow.sql', 'w') as f:
    f.write(sql)

print(f"SQL update file generated. Cred ID: {CRED_ID}, Error WF ID: {ERROR_WF_ID}")
