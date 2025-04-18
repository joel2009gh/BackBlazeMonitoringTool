#!/usr/bin/env python3
import os
import time
import json
import argparse
import subprocess
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

DEFAULT_CONFIG = {
    'bucket_name': 'BUCKET',
    'check_interval': '300', # Default
    'current_file': 'current_files.txt',
    'previous_file': 'previous_files.txt',
    'email': {
        'smtp_server': 'smtp',
        'smtp_port': '',
        'sender': 'example@example.com',
        'password': '',
        'recipients': [
            'example@example.com',
            'example@example.com'
        ],
        'subject': 'Changes in Backblaze Storage'
    }
}

CONFIG_FILE = 'config.json'

def create_default_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)
    print(f"Default configuration file created at {CONFIG_FILE}")
    print("Please edit this file with your settings before running the script again.")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Configuration file {CONFIG_FILE} not found. Using default configuration.")
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading configuration file: {e}")
        print("Using default configuration.")
        return DEFAULT_CONFIG

def get_all_files_to_txt(config):
    try:
        cmd = f"b2 ls --recursive b2://{config['bucket_name']} > {config['current_file']}"
        result = os.system(cmd)
        if result != 0:
            return False
        with open(config['current_file'], 'r') as f:
            line_count = sum(1 for _ in f)
        print(f"Retrieved {line_count} files from bucket")
        return True
    except Exception as e:
        return False

def backup_current_to_previous(config):
    if os.path.exists(config['current_file']):
        try:
            cmd = f"cp {config['current_file']} {config['previous_file']}"
            os.system(cmd)
            return True
        except Exception:
            return False
    return False

def compare_files(config):
    if not os.path.exists(config['current_file']) or not os.path.exists(config['previous_file']):
        return None
    try:
        with open(config['current_file'], 'r') as f:
            current_lines = set(f.read().splitlines())
        with open(config['previous_file'], 'r') as f:
            previous_lines = set(f.read().splitlines())
        added = current_lines - previous_lines
        removed = previous_lines - current_lines
        print(f"Comparison: {len(added)} new files, {len(removed)} removed files")
        return {
            'added': list(added),
            'removed': list(removed)
        }
    except Exception:
        return None

def send_email(changes, config):
    if not changes or (not changes['added'] and not changes['removed']):
        return
    try:
        subject = config['email']['subject']
        body = "Changes in Backblaze storage:\n\n"
        if changes['added']:
            body += f"New files ({len(changes['added'])}):\n"
            for line in changes['added'][:20]:
                body += f"+ {line}\n"
            if len(changes['added']) > 20:
                body += f"... and {len(changes['added']) - 20} more\n"
        if changes['removed']:
            body += f"\nRemoved files ({len(changes['removed'])}):\n"
            for line in changes['removed'][:20]:
                body += f"- {line}\n"
            if len(changes['removed']) > 20:
                body += f"... and {len(changes['removed']) - 20} more\n"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = config['email']['sender']
        msg['To'] = ", ".join(config['email']['recipients'])
        server = smtplib.SMTP(config['email']['smtp_server'], config['email']['smtp_port'])
        server.starttls()
        server.login(config['email']['sender'], config['email']['password'])
        server.send_message(msg)
        server.quit()
        # Debug line
        print(f"Email sent to {len(config['email']['recipients'])} recipients")
        return True
    except Exception:
        return False

def monitor_files(config):
    print(f"Monitoring started for bucket {config['bucket_name']}")
    if not os.path.exists(config['previous_file']):
        if get_all_files_to_txt(config):
            backup_current_to_previous(config)
    while True:
        try:
            if not get_all_files_to_txt(config):
                time.sleep(60)
                continue
            changes = compare_files(config)
            if changes and (changes['added'] or changes['removed']):
                send_email(changes, config)
            backup_current_to_previous(config)
            time.sleep(config['check_interval'])
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor Backblaze B2 bucket for file changes')
    parser.add_argument('--first-run', action='store_true', help='Create default config.json and exit')
    args = parser.parse_args()
    if args.first_run:
        create_default_config()
    else:
        config = load_config()
        monitor_files(config)
