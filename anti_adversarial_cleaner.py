import os
import shutil
import json
import datetime

ORIGINAL_DIR = 'original_files'
RECOVERED_DIR = 'recovered_files'
LOG_FILE = 'recovery_log.json'
os.makedirs(RECOVERED_DIR, exist_ok=True)

recovery_log = []

def log_recovery(file, file_type):
    recovery_log.append({
        "filename": file,
        "action": "recovered",
        "file_type": file_type,
        "timestamp": datetime.datetime.now().isoformat()
    })

def get_file_type(file):
    if file.endswith(('.png', '.jpg', '.jpeg')):
        return 'image'
    elif file.endswith('.txt'):
        return 'text'
    elif file.endswith('.pdf'):
        return 'pdf'
    return 'unknown'

def recover_files():
    count = 0
    for filename in os.listdir(ORIGINAL_DIR):
        src = os.path.join(ORIGINAL_DIR, filename)
        dst = os.path.join(RECOVERED_DIR, f"recovered_{filename}")
        shutil.copy2(src, dst)
        log_recovery(filename, get_file_type(filename))
        count += 1
    with open(LOG_FILE, 'w') as f:
        json.dump(recovery_log, f, indent=2)
    print(f" Recovery log saved to: {LOG_FILE}")
    print(f" {count} files recovered to '{RECOVERED_DIR}'")

if __name__ == "__main__":
    confirm = input("Recover original versions? (yes/no): ").strip().lower()
    if confirm == 'yes':
        recover_files()
    else:
        print("Recovery aborted.")
