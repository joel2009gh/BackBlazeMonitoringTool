# These are the things you need to do before you can run this script (I assume you already have python installed, if not: sudo apt install python3):
 1. Make a virtual env: python3 -m venv ~/b2_env
 2. Activate the env: source ~/b2_env/bin/activate
 3. You want the packages list to be up to date, so run this: sudo apt update
 4. Install b2: pip install b2
 5. Sign into the account, do this with: b2 account authorize
 6. Run this script for the first time with: python3 b2monitoring.py --first-run.
 7. This will create a .json file, called config.json, edit this .json to your favor
 8. Run this script as default: python3 b2monitoring.py (without a 2th argument)

# Possible error messages:
 1. pip: command not found/not installed
 Solution: sudo apt install python3-pip
 2. ModuleNotFoundError: No module named 'venv'
 Solution: sudo apt install python3-venv
 3. source: command not found (when activating)
 Solution: . ~/b2_env/bin/activate
 4. sh: 1: cannot create current_files.txt: Permission denied
 Solution: run script(s) with sudo

# !!! You can install everything at once if you run!!!:
1. chmod +x setup_b2_tool.sh
2. sudo ./setup_b2_tool.sh
3. Edit config.json
4. Run python3 b2monitoring.py

6. # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
