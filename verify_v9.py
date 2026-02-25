import json
with open('main_v9.json', 'r') as f:
    d = json.load(f)
q = [n['parameters']['query'] for n in d['nodes'] if n['name'] == 'Update DB'][0]
if "/g" in q:
    print("Found /g")
else:
    print("Not found /g")
print(f"Full query part: {q[:200]}")
