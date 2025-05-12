# -*- coding: utf-8 -*-
"""
Created on Mon May 12 17:53:04 2025

@author: USER
"""

import os

DISTORTED_DIR = 'distorted_files'

def cleanup():
    count = 0
    for file in os.listdir(DISTORTED_DIR):
        if file.startswith('distorted_'):
            os.remove(os.path.join(DISTORTED_DIR, file))
            count += 1
    print(f"Clean-up complete. {count} distorted files removed.")

if __name__ == "__main__":
    confirm = input("Are you sure you want to remove all distorted files? (yes/no): ").strip().lower()
    if confirm == 'yes':
        cleanup()
    else:
        print("Clean-up aborted.")
