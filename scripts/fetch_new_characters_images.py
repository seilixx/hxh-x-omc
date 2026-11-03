import urllib.request
import urllib.parse
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

wiki_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HunterQuiz/2.0",
    "Referer": "https://en.wikipedia.org/"
}

anilist_headers = {
    "User-Agent": "HunterQuiz/2.0",
    "Content-Type": "application/json"
}

def dl_wiki(title, dest_path):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    try:
        req = urllib.request.Request(url, headers=wiki_headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read())
            img_url = data.get("thumbnail", {}).get("source") or data.get("originalimage", {}).get("source")
            if not img_url:
                print(f"[WIKI FAIL] No image for {title}")
                return False
            img_url = img_url.split("?")[0]
            img_req = urllib.request.Request(img_url, headers=wiki_headers)
            with urllib.request.urlopen(img_req, timeout=12) as img_res:
                content = img_res.read()
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, "wb") as f:
                    f.write(content)
            print(f"[WIKI OK] {title} -> {dest_path} ({len(content)} bytes)")
            return True
    except Exception as e:
        print(f"[WIKI ERR] {title}: {e}")
        return False

def dl_direct(url, dest_path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as res:
            content = res.read()
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "wb") as f:
                f.write(content)
        print(f"[DIRECT OK] {dest_path} ({len(content)} bytes)")
        return True
    except Exception as e:
        print(f"[DIRECT ERR] {dest_path}: {e}")
        return False

# 1. NEW FOOTBALL PLAYERS (fb-031 to fb-050)
FOOTBALL_TARGETS = [
    ("fb-031.jpg", "Lev Yashin"),
    ("fb-032.jpg", "Ferenc Puskás"),
    ("fb-033.jpg", "Alfredo Di Stéfano"),
    ("fb-034.jpg", "Eusébio"),
    ("fb-035.jpg", "George Best"),
    ("fb-036.jpg", "Franz Beckenbauer"),
    ("fb-037.jpg", "Johan Cruyff"),
    ("fb-038.jpg", "Michel Platini"),
    ("fb-039.jpg", "Marco van Basten"),
    ("fb-040.jpg", "Franco Baresi"),
    ("fb-041.jpg", "Paolo Maldini"),
    ("fb-042.jpg", "Andrea Pirlo"),
    ("fb-043.jpg", "Luka Modrić"),
    ("fb-044.jpg", "Roberto Carlos"),
    ("fb-045.jpg", "Dennis Bergkamp"),
    ("fb-046.jpg", "Ruud Gullit"),
    ("fb-047.jpg", "Lothar Matthäus"),
    ("fb-048.jpg", "Oliver Kahn"),
    ("fb-049.jpg", "Dino Zoff"),
    ("fb-050.jpg", "Garrincha"),
]

print("=== FETCHING NEW FOOTBALL IMAGES ===")
for filename, title in FOOTBALL_TARGETS:
    dest = os.path.join("public", "assets", "characters", "football", filename)
    dl_wiki(title, dest)
    time.sleep(0.3)

# 2. NEW MARVEL HEROES (marvel-031 to marvel-050)
MARVEL_TARGETS = [
    ("marvel-031.jpg", "Doctor Doom"),
    ("marvel-032.jpg", "Magneto (Marvel Comics)"),
    ("marvel-033.jpg", "Galactus"),
    ("marvel-034.jpg", "Silver Surfer"),
    ("marvel-035.jpg", "Kang the Conqueror"),
    ("marvel-036.jpg", "Daredevil (Marvel Comics character)"),
    ("marvel-037.jpg", "Punisher"),
    ("marvel-038.jpg", "Blade (character)"),
    ("marvel-039.jpg", "Ghost Rider"),
    ("marvel-040.jpg", "Moon Knight (character)"),
    ("marvel-041.jpg", "Namor"),
    ("marvel-042.jpg", "Ultron"),
    ("marvel-043.jpg", "Hela (Marvel Comics)"),
    ("marvel-044.jpg", "Adam Warlock"),
    ("marvel-045.jpg", "Gorr the God Butcher"),
    ("marvel-046.jpg", "Carnage (character)"),
    ("marvel-047.jpg", "Mysterio"),
    ("marvel-048.jpg", "Apocalypse (character)"),
    ("marvel-049.jpg", "MODOK"),
    ("marvel-050.jpg", "Emma Frost"),
]

print("\n=== FETCHING NEW MARVEL IMAGES ===")
for filename, title in MARVEL_TARGETS:
    dest = os.path.join("public", "assets", "characters", "marvel", filename)
    dl_wiki(title, dest)
    time.sleep(0.3)

print("\nDone fetching Football and Marvel images!")

