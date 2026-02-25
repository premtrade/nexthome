import json
import subprocess

# Define the fixed credential structure
fixed_creds = [
  {
    "id": "UiVjly5vgM3yn3AG",
    "name": "Postgres account",
    "type": "postgres",
    "data": {
      "host": "db",
      "port": 5432,
      "database": "saas_db",
      "user": "n8n_user",
      "password": "n8n_password",
      "ssl": "disable"
    }
  }
]

# Write to a local file
with open('fixed_creds.json', 'w') as f:
    json.dump(fixed_creds, f, indent=2)

# Copy to docker and import
try:
    subprocess.run(["docker", "cp", "fixed_creds.json", "next_home_n8n:/home/node/fixed_creds.json"], check=True)
    # Using --input instead of --path
    subprocess.run(["docker", "exec", "next_home_n8n", "n8n", "import:credentials", "--input=/home/node/fixed_creds.json"], check=True)
    print("Credentials re-imported successfully.")
except Exception as e:
    print(f"Failed to re-import credentials: {e}")
