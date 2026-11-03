import urllib.request
import urllib.parse
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HunterQuizLegends/2.1 (contact: test@example.com)",
    "Referer": "https://en.wikipedia.org/"
}

MISSING_TARGETS = [
    # Football
    ("football/fb-045.jpg", "Dennis Bergkamp"),
    ("football/fb-046.jpg", "Ruud Gullit"),
    ("football/fb-047.jpg", "Lothar Matthäus"),
    ("football/fb-048.jpg", "Oliver Kahn"),
    ("football/fb-049.jpg", "Dino Zoff"),
    
    # Marvel
    ("marvel/marvel-031.jpg", "Doctor Doom"),
    ("marvel/marvel-032.jpg", "Magneto (Marvel Comics)"),
    ("marvel/marvel-033.jpg", "Galactus"),
    ("marvel/marvel-034.jpg", "Silver Surfer"),
    ("marvel/marvel-036.jpg", "Daredevil (Marvel Comics character)"),
    ("marvel/marvel-037.jpg", "Punisher"),
    ("marvel/marvel-038.jpg", "Blade (character)"),
    ("marvel/marvel-039.jpg", "Ghost Rider"),
    ("marvel/marvel-040.jpg", "Moon Knight (character)"),
    ("marvel/marvel-041.jpg", "Namor"),
    ("marvel/marvel-042.jpg", "Ultron"),
    ("marvel/marvel-043.jpg", "Hela (Marvel Comics)"),
    ("marvel/marvel-044.jpg", "Adam Warlock"),
    ("marvel/marvel-050.jpg", "Emma Frost"),
]

def fetch_wiki(rel_path, title):
    dest = os.path.join("public", "assets", "characters", rel_path)
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        print(f"[EXISTS] {rel_path}")
        return True
    
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as res:
                data = json.loads(res.read())
                img_url = data.get("thumbnail", {}).get("source") or data.get("originalimage", {}).get("source")
                if not img_url:
                    print(f"[NO IMG] {title}")
                    return False
                img_url = img_url.split("?")[0]
                
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=12) as img_res:
                    content = img_res.read()
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    with open(dest, "wb") as f:
                        f.write(content)
                print(f"[SAVED] {rel_path} ({len(content)} bytes)")
                return True
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = (attempt + 1) * 3
                print(f"[429 WAIT] {title} waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"[HTTP {e.code}] {title}")
                return False
        except Exception as e:
            print(f"[ERR] {title}: {e}")
            time.sleep(2)
    return False

for rel_path, title in MISSING_TARGETS:
    fetch_wiki(rel_path, title)
    time.sleep(1.8)

print("Remaining wiki fetch done!")

