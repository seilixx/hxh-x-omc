import urllib.request
import json
import urllib.parse
import os
import sys
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://en.wikipedia.org/"
}

FOOTBALL_FIXES = [
    ("fb-014.jpg", "Mohamed Salah"),
    ("fb-015.jpg", "Thierry Henry"),
    ("fb-017.jpg", "Xavi Hernández"),
    ("fb-022.jpg", "Kaká"),
    ("fb-024.jpg", "Sergio Ramos"),
    ("fb-026.jpg", "Toni Kroos"),
    ("fb-028.jpg", "Vinícius Júnior"),
]

MARVEL_FIXES = [
    ("marvel-002.jpg", "Captain America"),
    ("marvel-011.jpg", "Scarlet Witch"),
    ("marvel-021.jpg", "Professor X"),
]

def download_wiki_thumbnail(title, dest_path):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read())
            img_url = data.get("thumbnail", {}).get("source") or data.get("originalimage", {}).get("source")
            if not img_url:
                print(f"[FAIL] No image for {title}")
                return False
            # remove query parameters
            img_url = img_url.split("?")[0]
            print(f"[DOWNLOADING] {title} -> {img_url}")
            
            img_req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(img_req, timeout=12) as img_res:
                content = img_res.read()
                with open(dest_path, "wb") as f:
                    f.write(content)
            print(f"[SUCCESS] Saved {dest_path} ({len(content)} bytes)")
            return True
    except Exception as e:
        print(f"[ERR] {title}: {e}")
        return False

print("=== FIXING FOOTBALL IMAGES ===")
for filename, title in FOOTBALL_FIXES:
    dest = os.path.join("public", "assets", "characters", "football", filename)
    download_wiki_thumbnail(title, dest)

print("\n=== FIXING MARVEL IMAGES ===")
for filename, title in MARVEL_FIXES:
    dest = os.path.join("public", "assets", "characters", "marvel", filename)
    download_wiki_thumbnail(title, dest)

print("\nDone fixing images!")

