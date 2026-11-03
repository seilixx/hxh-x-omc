import os
import glob
from PIL import Image

for folder in ['hunter-x-hunter', 'naruto', 'jujutsu-kaisen', 'one-piece']:
    files = glob.glob(f"public/assets/characters/{folder}/*.jpg")
    print(f"{folder}: {len(files)} image files")
    for fp in files:
        sz = os.path.getsize(fp)
        try:
            with Image.open(fp) as im:
                w, h = im.size
                if w < 50 or h < 50 or sz < 2000:
                    print(f"  Suspicious size: {fp} ({w}x{h}, {sz} bytes)")
        except Exception as e:
            print(f"  CORRUPT: {fp} - {e}")
