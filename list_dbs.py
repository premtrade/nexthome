import subprocess

cmd = ["docker", "exec", "next_home_db", "psql", "-U", "n8n_user", "-c", "\\l"]
print(subprocess.check_output(cmd).decode('utf-8'))
