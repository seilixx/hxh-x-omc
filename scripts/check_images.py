import re
import glob
import os

files = glob.glob('src/data/**/characters.ts', recursive=True)
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    pattern = r"id:\s*'([^']+)'[\s\S]*?name:\s*'([^']+)'[\s\S]*?image:\s*'([^']+)'"
    chars = re.findall(pattern, content)
    print(f"\n--- {f} (Total: {len(chars)}) ---")
    missing = 0
    for cid, name, img in chars:
        if img.startswith('/'):
            local_path = os.path.join('public', img.lstrip('/'))
            if not os.path.exists(local_path):
                print(f"  MISSING FILE: {cid} ({name}) -> {img}")
                missing += 1
            else:
                size = os.path.getsize(local_path)
                if size < 1000:
                    print(f"  TINY FILE ({size}b): {cid} ({name}) -> {img}")
        else:
            print(f"  EXTERNAL URL: {cid} ({name}) -> {img}")
    if missing == 0:
        print("  All local files exist!")
