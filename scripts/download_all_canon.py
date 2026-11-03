import urllib.request
import os

UPDATES = [
    ("public/assets/characters/jujutsu-kaisen/jjk-024.jpg", "https://s4.anilist.co/file/anilistcdn/character/large/b162722-btzdghBizxKS.jpg"), # Toji Fushiguro
    ("public/assets/characters/jujutsu-kaisen/jjk-025.jpg", "https://s4.anilist.co/file/anilistcdn/character/large/b156991-niYjdp9CxO4w.png"), # Jogo
    ("public/assets/characters/one-piece/op-023.jpg", "https://s4.anilist.co/file/anilistcdn/character/large/b3331-7ZJDc4BNv9Yp.jpg"), # Marshall D. Teach
    ("public/assets/characters/one-piece/op-024.jpg", "https://s4.anilist.co/file/anilistcdn/character/large/b17142-OXOpztWZIE2A.png"), # Silvers Rayleigh
    ("public/assets/characters/hunter-x-hunter/hxh-045.jpg", "https://s4.anilist.co/file/anilistcdn/character/large/33300.jpg"), # Genthru
    ("public/assets/characters/hunter-x-hunter/hxh-047.jpg", "https://s4.anilist.co/file/anilistcdn/character/large/29808.jpg"), # Meleoron
    ("public/assets/characters/hunter-x-hunter/hxh-017.jpg", "https://s4.anilist.co/file/anilistcdn/character/large/b29809-wAoam5TkZilJ.png"), # Knuckle Bine
    ("public/assets/characters/hunter-x-hunter/hxh-044.jpg", "https://s4.anilist.co/file/anilistcdn/character/large/82925.jpg"), # Knov
    ("public/assets/characters/hunter-x-hunter/hxh-031.jpg", "https://s4.anilist.co/file/anilistcdn/character/large/b5835-cbomgYG3LWrP.jpg"), # Pakunoda
]

for dest, url in UPDATES:
    print(f"Downloading {url} -> {dest}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Antigravity"})
    with urllib.request.urlopen(req) as res, open(dest, "wb") as f:
        f.write(res.read())
    print(f"  OK ({os.path.getsize(dest)} bytes)")

print("All updated images downloaded successfully!")
