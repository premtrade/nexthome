import sqlite3
import json

conn = sqlite3.connect('flowise_db_tmp.sqlite')
cur = conn.cursor()

# Get existing embedding node config
cur.execute("SELECT flowData FROM chat_flow WHERE id = '8a8328f8-352c-4344-8be5-b4dabacb4656'")
row = cur.fetchone()
if not row:
    print("Not found")
    exit()

data = json.loads(row[0])
# Add a Conversation Chain and a ChatOpenAI (as it's required for the chain, even if we just want embeddings)
# Actually, Flowise has a "Vector Store" nodes. 
# Better: Just make it a "Conversation Chain" with a dummy LLM and the embedding model as a tool? No.

# NEW STRATEGY: Create a NEW chatflow that is a "Buffer Memory" + "Conversation Chain" + "Groq" LLM.
# We'll use it just to prove the chain works.

# Actually, I'll just fix the existing one to be a Chain.
new_nodes = [
    {
        "id": "huggingFaceInferenceEmbeddings_0",
        "type": "customNode",
        "data": {
            "label": "HuggingFace Inference Embeddings",
            "name": "huggingFaceInferenceEmbeddings",
            "version": 1,
            "inputs": {
                "modelName": "sentence-transformers/all-MiniLM-L6-v2"
            }
        },
        "position": {"x": 100, "y": 100}
    },
    {
        "id": "chatGroq_0",
        "type": "customNode",
        "data": {
            "label": "ChatGroq",
            "name": "chatGroq",
            "version": 1,
            "inputs": {
                "modelName": "mixtral-8x7b-32768"
            },
            "credential": "97bbb0a2-42ca-4d6e-8488-e38b3cff3c42"
        },
        "position": {"x": 100, "y": 400}
    },
    {
        "id": "conversationChain_0",
        "type": "customNode",
        "data": {
            "label": "Conversation Chain",
            "name": "conversationChain",
            "version": 2,
            "inputs": {
                "model": "={{chatGroq_0}}",
                "memory": "={{bufferMemory_0}}"
            }
        },
        "position": {"x": 500, "y": 250}
    },
    {
        "id": "bufferMemory_0",
        "type": "customNode",
        "data": {
            "label": "Buffer Memory",
            "name": "bufferMemory",
            "version": 1
        },
        "position": {"x": 500, "y": 100}
    }
]
data['nodes'] = new_nodes
# Edges (simplified for this script)
data['edges'] = [] # Usually handled by inputs references in newer Flowise versions

cur.execute("UPDATE chat_flow SET flowData = ? WHERE id = '8a8328f8-352c-4344-8be5-b4dabacb4656'", (json.dumps(data),))
conn.commit()
conn.close()
print("Updated chatflow 8a8 to be a Chain.")
