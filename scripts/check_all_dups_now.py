import hashlib
import glob
import os

for folder in sorted(glob.glob('public/assets/characters/*')):
    if not os.path.isdir(folder): continue
    hashes = {}
    for img in sorted(glob.glob(os.path.join(folder, '*.*'))):
        with open(img, 'rb') as f:
            h = hashlib.md5(f.read()).hexdigest()
        hashes.setdefault(h, []).append(os.path.basename(img))
    
    dups = [files for h, files in hashes.items() if len(files) > 1]
    if dups:
        print(f"=== {os.path.basename(folder)}: {len(dups)} DUPLICATE GROUPS ===")
        for d in dups:
            print(f"  Duplicates: {d}")
    else:
        print(f"=== {os.path.basename(folder)}: 0 DUPLICATES (ALL UNIQUE!) ===")

