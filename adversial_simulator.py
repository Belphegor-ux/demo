import os
import random
import shutil
from PIL import Image
import numpy as np
from PyPDF2 import PdfReader, PdfWriter

ORIGINAL_DIR = 'original_files'
DISTORTED_DIR = 'distorted_files'
os.makedirs(DISTORTED_DIR, exist_ok=True)

def distort_image(image_path, output_path):
    img = Image.open(image_path).convert('RGB')
    np_img = np.array(img)
    # Stronger Gaussian noise
    noise = np.random.normal(0, 50, np_img.shape).astype(np.int16)
    noisy_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
    result_img = Image.fromarray(noisy_img)
    result_img.save(output_path)

def distort_text(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # Random distortion: change case and add symbols
    distorted = ''.join(random.choice((c.upper(), c.lower(), '*', '#')) for c in text)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(distorted)

def distort_pdf(file_path, output_path):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        content = page.extract_text() or ""
        # Add distortion: insert noise symbols
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
                print(f"[✓] Distorted image: {filename}")
            elif ext.endswith('.txt'):
                distort_text(src_path, dst_path)
                print(f"[✓] Distorted text: {filename}")
            elif ext.endswith('.pdf'):
                distort_pdf(src_path, dst_path)
                print(f"[✓] Distorted PDF: {filename}")
            else:
                print(f"[!] Skipping unsupported file: {filename}")
        except Exception as e:
            print(f"[X] Failed to distort {filename}: {e}")

if __name__ == "__main__":
    print(" Running simulated adversarial attack...")
    simulate_attack()
    print(" Distorted files saved to:", DISTORTED_DIR)
