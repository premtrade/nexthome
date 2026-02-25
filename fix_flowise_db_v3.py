import sqlite3
import json
import os
import re

db_path = 'flowise_db_tmp.sqlite'

def fix_db():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("SELECT id, flowData FROM chat_flow")
    rows = cur.fetchall()
    
    for row_id, flow_json in rows:
        flow_data = json.loads(flow_json)
        changed = False
        
        for node in flow_data['nodes']:
            inputs = node['data'].get('inputs', {})
            for key in list(inputs.keys()):
                val = inputs[key]
                if isinstance(val, str) and key in ['systemMessage', 'systemMessagePrompt', 'template', 'prompt']:
                    # Remove ANY line containing { or } to avoid LangChain template issues
                    new_val = re.sub(r'.*[{}].*\n?', '', val)
                    if new_val != val:
                        print(f"Fixed {key} in flow {row_id}")
                        inputs[key] = new_val
                        changed = True
        
        if changed:
            new_json = json.dumps(flow_data)
            cur.execute("UPDATE chat_flow SET flowData = ? WHERE id = ?", (new_json, row_id))
            
    conn.commit()
    conn.close()

fix_db()
