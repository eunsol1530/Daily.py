import subprocess
import datetime

# Database connection details
database_host = "localhost"
database_port = 5432
database_name = "your_database_name"
database_user = "your_username"
database_password = "your_password"

# Backup destination directory
backup_directory = "/path/to/backup/directory/"

# Generate a timestamp for the backup filename
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Create the backup filename
backup_filename = f"{database_name}_backup_{timestamp}.sql"

# Command to perform the backup
backup_command = [
    "pg_dump",
    f"--host={database_host}",
    f"--port={database_port}",
    f"--username={database_user}",
    "--password",
    f"--dbname={database_name}",
    f"--file={backup_directory}{backup_filename}"
]

# Execute the backup command
subprocess.run(backup_command, shell=False)

# Print success message
print(f"Database backup created: {backup_filename}")
