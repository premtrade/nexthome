import requests
import json

try:
    # Use the service name from docker-compose if running inside docker, 
    # but here I am on the host. docker-compose says qdrant is on 6333.
    r = requests.post("http://localhost:6333/collections/properties/points/count", json={})
    print(r.json())
except Exception as e:
    print(f"Error: {e}")
