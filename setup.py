import os
import subprocess
import sys
import venv

# Function to print messages
def print_message(message):
    print(f"\n{'=' * 40}\n{message}\n{'=' * 40}\n")

# Step 1: Create the virtual environment
venv_dir = os.path.join(os.getcwd(), 'venv')
print_message(f"Creating virtual environment in {venv_dir}...")
venv.create(venv_dir, with_pip=True)
print_message("Virtual environment created successfully.")

# Step 2: Install requirements from requirements.txt
requirements_file = 'requirements.txt'
if not os.path.exists(requirements_file):
    print_message(f"Error: {requirements_file} not found!")
    sys.exit(1)

pip_executable = os.path.join(venv_dir, 'bin', 'pip') if os.name != 'nt' else os.path.join(venv_dir, 'Scripts', 'pip.exe')

print_message(f"Installing packages from {requirements_file} using {pip_executable}...")
subprocess.check_call([pip_executable, 'install', '-r', requirements_file])
print_message("Packages installed successfully.")

# Step 3: Provide final instructions to the user
if os.name == 'nt':
    activate_script = os.path.join(venv_dir, 'Scripts', 'activate.bat')
else:
    activate_script = os.path.join(venv_dir, 'bin', 'activate')

print_message(f"Setup completed.\nTo activate the virtual environment, run:\nsource {activate_script}\n")
