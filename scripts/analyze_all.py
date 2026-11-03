import json
import re
import os
import glob
import hashlib

def get_chars(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Match id, name, difficulty, image
    # Use regex or simple parse
    pattern = r'\{\s*"id":\s*"([^"]+)",\s*"name":\s*"([^"]+)",(?:.|\n)*?"difficulty":\s*"([^"]+)",(?:.|\n)*?"image":\s*"([^"]+)"'
    # Fallback to single quotes if needed
    matches = re.findall(pattern, content)
    if not matches:
        pattern2 = r'\{\s*id:\s*\'([^\']+)\',\s*name:\s*\'([^\']+)\',(?:.|\n)*?difficulty:\s*\'([^\']+)\',(?:.|\n)*?image:\s*\'([^\']+)\''
        matches = re.findall(pattern2, content)
    return matches

print("=== CHARACTER COUNTS & DIFFICULTIES ===")
for folder in ['hunter-x-hunter', 'naruto', 'jujutsu-kaisen', 'one-piece', 'marvel', 'football']:
    path = f'src/data/{folder}/characters.ts'
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    diffs = re.findall(r'difficulty[\'"]?\s*:\s*[\'"](\w+)[\'"]', text)
    counts = {}
    for d in diffs:
        counts[d] = counts.get(d, 0) + 1
    total = len(diffs)
    print(f"{folder:16} Total: {total:3} | {counts}")

print("\n=== FOOTBALL DUPLICATES ===")
dups = ['fb-001', 'fb-014', 'fb-015', 'fb-017', 'fb-022', 'fb-024', 'fb-026', 'fb-028']
with open('src/data/football/characters.ts', 'r', encoding='utf-8') as f:
    text = f.read()
blocks = re.split(r'\n\s*\{\s*\n', text)
for b in blocks:
    id_m = re.search(r'["\']id["\']:\s*["\']([^"\']+)["\']', b)
    name_m = re.search(r'["\']name["\']:\s*["\']([^"\']+)["\']', b)
    wiki_m = re.search(r'["\']wiki["\']:\s*["\']([^"\']+)["\']', b)
    if id_m and name_m:
        cid = id_m.group(1)
        if cid in dups:
            print(f"{cid}: {name_m.group(1)} (wiki: {wiki_m.group(1) if wiki_m else 'None'})")

