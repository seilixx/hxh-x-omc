import urllib.request
import json
import urllib.parse
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

from build_marvel_and_football import MARVEL_CHARACTERS, FOOTBALL_PLAYERS

# Fallback direct image URLs for any that Wikimedia throttled
FALLBACK_MARVEL = {
    "Iron Man": "https://upload.wikimedia.org/wikipedia/en/4/47/Iron_Man_%28circa_2018%29.png",
    "Captain America": "https://upload.wikimedia.org/wikipedia/en/b/b9/Captain_America_Vol_9_1_Cover.jpg",
    "Wolverine": "https://upload.wikimedia.org/wikipedia/en/d/d3/Wolverine_%28circa_2024%29.jpg",
    "Doctor Strange": "https://upload.wikimedia.org/wikipedia/en/4/4f/Doctor_Strange_Vol_4_2_Ross_Variant_Textless.jpg",
    "Scarlet Witch": "https://upload.wikimedia.org/wikipedia/en/9/97/Scarlet_Witch_%28circa_2023%29.png",
    "Deadpool": "https://upload.wikimedia.org/wikipedia/en/c/ca/Deadpool.png",
    "Groot": "https://upload.wikimedia.org/wikipedia/en/b/b5/I_am_Groot_vol_1_1.png",
    "Professor X": "https://upload.wikimedia.org/wikipedia/en/a/a2/Professor_X_%28circa_2019%29.png",
    "Green Goblin": "https://upload.wikimedia.org/wikipedia/en/3/35/Green_Goblin_Comic_Art_by_Miguel_Mercado.png",
    "Vision": "https://upload.wikimedia.org/wikipedia/en/3/3d/Vision_%28Marvel_Comics%29.png",
    "Captain Marvel": "https://upload.wikimedia.org/wikipedia/en/0/02/Carol_Danvers_-_%28evolution%29.jpg",
}

def download_file(url, dest):
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    "Referer": "https://en.wikipedia.org/"
                }
            )
            with urllib.request.urlopen(req, timeout=12) as res:
                content = res.read()
                with open(dest, "wb") as f:
                    f.write(content)
            return True
        except Exception as e:
            time.sleep(2)
    return False

def get_wiki_img(wiki_title):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(wiki_title)}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
            with urllib.request.urlopen(req, timeout=8) as res:
                data = json.loads(res.read())
                img = data.get("thumbnail", {}).get("source") or data.get("originalimage", {}).get("source")
                if img:
                    return img.split("?")[0]
        except Exception as e:
            time.sleep(2)
    return None

print("Checking and downloading missing Marvel images...")
for c in MARVEL_CHARACTERS:
    dest = f"public/assets/characters/marvel/{c['id']}.jpg"
    c['image'] = f"/assets/characters/marvel/{c['id']}.jpg"
    c['anime'] = 'marvel'
    if not os.path.exists(dest) or os.path.getsize(dest) < 2000:
        url = FALLBACK_MARVEL.get(c['name']) or get_wiki_img(c['wiki'])
        if url:
            ok = download_file(url, dest)
            print(f"  Marvel {c['name']} -> {ok} ({os.path.getsize(dest) if ok else 0} bytes)")
        else:
            print(f"  Marvel {c['name']} -> No URL found")
        time.sleep(1)

print("\nChecking and downloading missing Football images...")
for p in FOOTBALL_PLAYERS:
    dest = f"public/assets/characters/football/{p['id']}.jpg"
    p['image'] = f"/assets/characters/football/{p['id']}.jpg"
    p['anime'] = 'football'
    if not os.path.exists(dest) or os.path.getsize(dest) < 2000:
        url = get_wiki_img(p['wiki'])
        if url:
            ok = download_file(url, dest)
            print(f"  Football {p['name']} -> {ok} ({os.path.getsize(dest) if ok else 0} bytes)")
        else:
            print(f"  Football {p['name']} -> No URL found")
        time.sleep(1)

# Write TypeScript files
def write_ts_file(data, output_file, var_name):
    lines = [
        "import type { Character } from '../../types';",
        "",
        f"export const {var_name}: Character[] = " + json.dumps(data, indent=2) + ";",
        "",
        f"export default {var_name};",
        ""
    ]
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {output_file} ({len(data)} items)")

write_ts_file(MARVEL_CHARACTERS, "src/data/marvel/characters.ts", "marvelCharacters")
write_ts_file(FOOTBALL_PLAYERS, "src/data/football/characters.ts", "footballCharacters")
