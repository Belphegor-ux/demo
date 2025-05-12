import os
import random
import json
import datetime
from PIL import Image
import numpy as np
from PyPDF2 import PdfReader, PdfWriter

ORIGINAL_DIR = 'original_files'
DISTORTED_DIR = 'distorted_files'
LOG_FILE = 'attack_log.json'
os.makedirs(DISTORTED_DIR, exist_ok=True)

log_entries = []

def log_action(file, action_type, file_type):
    log_entries.append({
        "filename": file,
        "action": action_type,
        "file_type": file_type,
        "timestamp": datetime.datetime.now().isoformat()
    })

def distort_image(image_path, output_path):
    img = Image.open(image_path).convert('RGB')
    np_img = np.array(img)
    noise = np.random.normal(0, 80, np_img.shape).astype(np.int16)
    noisy_img = np.clip(np_img + noise, 0, 355).astype(np.uint8)
    Image.fromarray(noisy_img).save(output_path)

def distort_text(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    distorted = ''.join(random.choice((c.upper(), c.lower(), '*', '#')) for c in text)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(distorted)

def distort_pdf(file_path, output_path):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        content = page.extract_text() or ""
        distorted_content = ''.join(random.choice((c, '*', '~', '@')) for c in content)
        writer.add_blank_page(width=page.mediabox.width, height=page.mediabox.height)
        writer.pages[-1].insert_text(distorted_content)
    with open(output_path, 'wb') as f:
        writer.write(f)

def simulate_attack():
    for filename in os.listdir(ORIGINAL_DIR):
        src_path = os.path.join(ORIGINAL_DIR, filename)
        dst_path = os.path.join(DISTORTED_DIR, f"distorted_{filename}")
        ext = filename.lower()
        try:
            if ext.endswith(('.png', '.jpg', '.jpeg')):
                distort_image(src_path, dst_path)
                log_action(filename, "distorted", "image")
            elif ext.endswith('.txt'):
                distort_text(src_path, dst_path)
                log_action(filename, "distorted", "text")
            elif ext.endswith('.pdf'):
                distort_pdf(src_path, dst_path)
                log_action(filename, "distorted", "pdf")
            else:
                print(f" Skipped unsupported file: {filename}")
        except Exception as e:
            print(f" Failed to distort {filename}: {e}")

  
    with open(LOG_FILE, 'w') as f:
        json.dump(log_entries, f, indent=2)
    print(f"Attack log saved to: {LOG_FILE}")

if __name__ == "__main__":
    print("⚠️ Running adversarial attack with logging...")
    simulate_attack()
    print("✅ Distorted files saved to:", DISTORTED_DIR)
