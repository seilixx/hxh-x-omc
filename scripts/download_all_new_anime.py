import urllib.request
import json
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/new_anime_urls.json', 'r', encoding='utf-8') as f:
    existing_urls = json.load(f)

# Specific exact AniList character IDs where search was ambiguous or missed
EXACT_IDS = {
    # Naruto
    "naruto-033": 3146, # Danzou Shimura
    "naruto-047": 32805, # A (Fourth Raikage)
    
    # One Piece
    "op-032": 20498, # Killer
    "op-043": 18937, # Gol D. Roger
    "op-046": 72467, # Kin'emon
    "op-049": 147514, # King
    "op-050": 147513, # Queen

    # JJK
    "jjk-036": 160417, # Junpei Yoshino
    "jjk-037": 196504, # Eso
    "jjk-038": 196505, # Kechizu
    "jjk-039": 208759, # Master Tengen
    "jjk-040": 218730, # Takako Uro
    "jjk-041": 218731, # Ryu Ishigori
    "jjk-042": 222131, # Reggie Star
    "jjk-043": 196507, # Ui Ui
    "jjk-044": 208761, # Arata Nitta
    "jjk-045": 196508, # Shiu Kong
    "jjk-046": 189238, # Miguel
}

query_by_id = """
query ($id: Int) {
  Character(id: $id) {
    id
    name { full }
    image { large }
  }
}
"""

def get_char_by_id(cid_num):
    req = urllib.request.Request(
        'https://graphql.anilist.co',
        data=json.dumps({'query': query_by_id, 'variables': {'id': cid_num}}).encode(),
        headers={'Content-Type': 'application/json', 'User-Agent': 'TargetedGetter/2.0'}
    )
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=8) as res:
                d = json.loads(res.read())
                return d['data']['Character']
        except Exception:
            time.sleep(1)
    return None

def download_img(url, dest):
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as res:
                content = res.read()
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, 'wb') as f:
                    f.write(content)
            return len(content)
        except Exception:
            time.sleep(1)
    return 0

# 1. Download existing matched anime URLs
print("=== DOWNLOADING MATCHED ANIME IMAGES ===")
for folder, chars in existing_urls.items():
    folder_name = 'naruto' if folder == 'naruto' else ('jujutsu-kaisen' if folder == 'jjk' else 'one-piece')
    for cid, info in chars.items():
        if cid in EXACT_IDS: # skip ambiguous ones
            continue
        dest = f"public/assets/characters/{folder_name}/{cid}.jpg"
        if os.path.exists(dest) and os.path.getsize(dest) > 5000:
            continue
        size = download_img(info['img'], dest)
        print(f"[{folder_name}] {cid} ({info['name']}) -> {size} bytes")
        time.sleep(0.15)

# 2. Download exact IDs
print("\n=== DOWNLOADING EXACT ID ANIME IMAGES ===")
for cid, anilist_id in EXACT_IDS.items():
    prefix = cid.split('-')[0]
    folder_name = 'naruto' if prefix == 'naruto' else ('jujutsu-kaisen' if prefix == 'jjk' else 'one-piece')
    dest = f"public/assets/characters/{folder_name}/{cid}.jpg"
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        continue
    c = get_char_by_id(anilist_id)
    if c and c.get('image', {}).get('large'):
        size = download_img(c['image']['large'], dest)
        print(f"[{folder_name} EXACT] {cid} ({c['name']['full']}) -> {size} bytes")
    else:
        print(f"[{folder_name} EXACT FAIL] {cid} ID {anilist_id}")
    time.sleep(0.3)

print("\nFinished downloading new anime images!")

