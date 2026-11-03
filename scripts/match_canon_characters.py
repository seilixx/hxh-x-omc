import json
import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/all_canon_characters.json', 'r', encoding='utf-8') as f:
    canon_db = json.load(f)

# Let's inspect each anime's current characters
def check_anime_characters(universe):
    filepath = f"src/data/{universe}/characters.ts"
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extract id and name
    blocks = re.findall(r'id:\s*\'([^\']+)\'[\s\S]*?name:\s*\'([^\']+)\'[\s\S]*?image:\s*\'([^\']+)\'', text)
    
    canon_list = canon_db.get(universe, {})
    
    print(f"\n==========================================")
    print(f"Checking {universe} ({len(blocks)} characters)")
    print(f"==========================================")
    
    matched = 0
    mismatched = []
    
    for cid, name, img in blocks:
        clean_name = name.lower().strip()
        # Direct match or partial match
        match = None
        if clean_name in canon_list:
            match = canon_list[clean_name]
        else:
            # Try matching parts or alternatives
            for ckey, cinfo in canon_list.items():
                if clean_name in ckey or ckey in clean_name:
                    match = cinfo
                    break
                # check alt names
                for alt in cinfo.get('alt', []):
                    if alt.lower() == clean_name or clean_name in alt.lower():
                        match = cinfo
                        break
                if match:
                    break
        
        if match:
            matched += 1
            print(f"[OK] {cid} '{name}' -> Canon ID {match['id']} ({match['full']})")
        else:
            mismatched.append((cid, name))
            print(f"[MISSING IN CANON LIST] {cid} '{name}'")
    
    print(f"Total matched: {matched}/{len(blocks)}")
    return mismatched

for u in ['naruto', 'hunter-x-hunter', 'jujutsu-kaisen', 'one-piece']:
    check_anime_characters(u)

