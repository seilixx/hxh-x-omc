import json
import urllib.request
import time
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

def parse_ts_characters(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Simple regex block parser
    # Match id, name, image, anime
    items = []
    # match each object
    blocks = re.split(r'\n\s*\{\s*\n', text)
    for b in blocks:
        id_m = re.search(r'["\']?id["\']?\s*:\s*["\']([^"\']+)["\']', b)
        name_m = re.search(r'["\']?name["\']?\s*:\s*["\']([^"\']+)["\']', b)
        img_m = re.search(r'["\']?image["\']?\s*:\s*["\']([^"\']+)["\']', b)
        diff_m = re.search(r'["\']?difficulty["\']?\s*:\s*["\']([^"\']+)["\']', b)
        if id_m and name_m and img_m:
            items.append({
                'id': id_m.group(1),
                'name': name_m.group(1),
                'image': img_m.group(1),
                'difficulty': diff_m.group(1) if diff_m else 'unknown'
            })
    return items

query = """
query ($search: String) {
  Character(search: $search) {
    id
    name { full native }
    media(type: ANIME, page: 1, perPage: 3) {
      nodes {
        id
        title { romaji english }
      }
    }
    image { large }
  }
}
"""

expected_keywords = {
    'hunter-x-hunter': ['hunter', 'hxh'],
    'naruto': ['naruto', 'boruto', 'shippuden'],
    'jujutsu-kaisen': ['jujutsu', 'jjk'],
    'one-piece': ['one piece'],
}

def check_universe(universe):
    filepath = f"src/data/{universe}/characters.ts"
    chars = parse_ts_characters(filepath)
    print(f"\n==========================================")
    print(f"Checking {universe} ({len(chars)} characters)...")
    print(f"==========================================")
    
    suspicious = []
    
    for c in chars:
        cid = c['id']
        name = c['name']
        
        # Test anilist search
        payload = json.dumps({'query': query, 'variables': {'search': name}}).encode()
        req = urllib.request.Request(
            'https://graphql.anilist.co',
            data=payload,
            headers={'Content-Type': 'application/json', 'User-Agent': 'AntigravityAudit/1.0'}
        )
        
        try:
            with urllib.request.urlopen(req, timeout=8) as res:
                data = json.loads(res.read())
                char_data = data.get('data', {}).get('Character')
                if not char_data:
                    suspicious.append((cid, name, "NOT FOUND on AniList"))
                    print(f"  [?] {cid} {name} -> NOT FOUND on AniList")
                    continue
                
                # Check media
                titles = []
                for m in char_data.get('media', {}).get('nodes', []):
                    t = m.get('title', {})
                    t_str = ((t.get('romaji') or '') + ' ' + (t.get('english') or '')).strip()
                    if t_str:
                        titles.append(t_str)
                
                combined = ' '.join(titles).lower()
                matched = any(kw in combined for kw in expected_keywords[universe])
                
                if not matched:
                    returned_name = char_data.get('name', {}).get('full')
                    suspicious.append((cid, name, returned_name, titles))
                    print(f"  [MISMATCH!] {cid} '{name}' -> returned '{returned_name}' from {titles[:2]}")
                else:
                    # Clean match
                    pass
        except Exception as e:
            print(f"  [ERR] {cid} {name}: {e}")
            time.sleep(1)
        
        time.sleep(0.35)
    
    return suspicious

results = {}
for u in ['naruto', 'hunter-x-hunter', 'jujutsu-kaisen', 'one-piece']:
    results[u] = check_universe(u)

with open('scripts/anime_mismatches.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n--- AUDIT COMPLETE ---")

