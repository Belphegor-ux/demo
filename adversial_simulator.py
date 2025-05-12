# -*- coding: utf-8 -*-
"""
Created on Mon May 12 17:51:23 2025

@author: USER
"""

import os
import shutil
import random
from PIL import Image, ImageFilter
import numpy as np

# Paths
ORIGINAL_DIR = 'original_files'
DISTORTED_DIR = 'distorted_files'
os.makedirs(DISTORTED_DIR, exist_ok=True)

def distort_image(image_path, output_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((img.width, img.height))  # force load
    np_img = np.array(img)

    # Add Gaussian noise
    noise = np.random.normal(0, 25, np_img.shape).astype(np.int16)
    noisy_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
    result_img = Image.fromarray(noisy_img)
    result_img.save(output_path)

def distort_text(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    
    distorted = ''.join(random.choice((c.upper(), c.lower(), '*', '#')) for c in text)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(distorted)

def simulate_attack():
    for filename in os.listdir(ORIGINAL_DIR):
        src_path = os.path.join(ORIGINAL_DIR, filename)
        dst_path = os.path.join(DISTORTED_DIR, f"distorted_{filename}")

        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            distort_image(src_path, dst_path)
            print(f"[✓] Distorted image: {filename}")
        elif filename.lower().endswith('.txt'):
            distort_text(src_path, dst_path)
            print(f"[✓] Distorted text: {filename}")
        else:
            print(f"[!] Skipping unsupported file: {filename}")

if __name__ == "__main__":
    print("Simulated adversarial attack running...")
    simulate_attack()
    print("Distorted copies saved to:", DISTORTED_DIR)
