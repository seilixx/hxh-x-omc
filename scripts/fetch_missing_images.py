import urllib.request
import json
import urllib.parse
import os
import time

# Missing Marvel targets:
# marvel-002: Captain America
# marvel-011: Scarlet Witch
# marvel-021: Professor X
# marvel-027: Green Goblin
# marvel-028: Vision

SPECIFIC_URLS = {
    "public/assets/characters/marvel/marvel-002.jpg": "https://upload.wikimedia.org/wikipedia/en/b/b9/Captain_America_Vol_9_1_Cover.jpg",
    "public/assets/characters/marvel/marvel-011.jpg": "https://upload.wikimedia.org/wikipedia/en/9/97/Scarlet_Witch_%28circa_2023%29.png",
    "public/assets/characters/marvel/marvel-021.jpg": "https://upload.wikimedia.org/wikipedia/en/a/a2/Professor_X_%28circa_2019%29.png",
    "public/assets/characters/marvel/marvel-027.jpg": "https://upload.wikimedia.org/wikipedia/en/3/35/Green_Goblin_Comic_Art_by_Miguel_Mercado.png",
    "public/assets/characters/marvel/marvel-028.jpg": "https://upload.wikimedia.org/wikipedia/en/3/3d/Vision_%28Marvel_Comics%29.png",
    "public/assets/characters/football/fb-007.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Ronaldinho_in_2019.jpg/330px-Ronaldinho_in_2019.jpg",
}

# Football remaining:
FB_WIKI_PAGES = [
    ("fb-011", "Kevin De Bruyne"),
    ("fb-012", "Robert Lewandowski"),
    ("fb-013", "Karim Benzema"),
    ("fb-014", "Mohamed Salah"),
    ("fb-015", "Thierry Henry"),
    ("fb-016", "Andrés Iniesta"),
    ("fb-017", "Xavi"),
    ("fb-018", "Gianluigi Buffon"),
    ("fb-019", "Virgil van Dijk"),
    ("fb-020", "Jude Bellingham"),
    ("fb-021", "Wayne Rooney"),
    ("fb-022", "Kaká"),
    ("fb-023", "Zlatan Ibrahimović"),
    ("fb-024", "Sergio Ramos"),
    ("fb-025", "Manuel Neuer"),
    ("fb-026", "Toni Kroos"),
    ("fb-027", "Harry Kane"),
    ("fb-028", "Vinícius Júnior"),
    ("fb-029", "Bukayo Saka"),
    ("fb-030", "Son Heung-min"),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://en.wikipedia.org/"
}

def dl(url, dest):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            with open(dest, "wb") as f:
                f.write(res.read())
        return True
    except Exception as e:
        return False

# 1. Download specific missing URLs
for dest, url in SPECIFIC_URLS.items():
    if not os.path.exists(dest) or os.path.getsize(dest) < 1000:
        dl(url, dest)
        time.sleep(0.5)

# 2. Download remaining football players
for fbid, title in FB_WIKI_PAGES:
    dest = f"public/assets/characters/football/{fbid}.jpg"
    if not os.path.exists(dest) or os.path.getsize(dest) < 1000:
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
        try:
            req = urllib.request.Request(summary_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as res:
                data = json.loads(res.read())
                img_url = data.get("thumbnail", {}).get("source") or data.get("originalimage", {}).get("source")
                if img_url:
                    img_url = img_url.split("?")[0]
                    dl(img_url, dest)
        except Exception:
            pass
        time.sleep(0.5)

m_cnt = len([f for f in os.listdir("public/assets/characters/marvel") if f.endswith(".jpg")])
fb_cnt = len([f for f in os.listdir("public/assets/characters/football") if f.endswith(".jpg")])
print(f"Total Marvel images on disk: {m_cnt}")
print(f"Total Football images on disk: {fb_cnt}")
