import urllib.request
import json
import os
import time

# Direct Wikimedia / public URLs for the remaining 3 Marvel and 11 Football:
DIRECT_URLS = {
    # Marvel
    "public/assets/characters/marvel/marvel-002.jpg": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Captain_America_Vol_9_1_Cover.jpg/330px-Captain_America_Vol_9_1_Cover.jpg",
    "public/assets/characters/marvel/marvel-011.jpg": "https://upload.wikimedia.org/wikipedia/en/thumb/9/97/Scarlet_Witch_%28circa_2023%29.png/330px-Scarlet_Witch_%28circa_2023%29.png",
    "public/assets/characters/marvel/marvel-021.jpg": "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Professor_X_%28circa_2019%29.png/330px-Professor_X_%28circa_2019%29.png",

    # Football
    "public/assets/characters/football/fb-007.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Ronaldinho_in_2019.jpg/330px-Ronaldinho_in_2019.jpg",
    "public/assets/characters/football/fb-011.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Kevin_De_Bruyne_201807091.jpg/330px-Kevin_De_Bruyne_201807091.jpg",
    "public/assets/characters/football/fb-014.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Mohamed_Salah_2018.jpg/330px-Mohamed_Salah_2018.jpg",
    "public/assets/characters/football/fb-015.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Thierry_Henry_2014.jpg/330px-Thierry_Henry_2014.jpg",
    "public/assets/characters/football/fb-016.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Andr%C3%A9s_Iniesta.jpg/330px-Andr%C3%A9s_Iniesta.jpg",
    "public/assets/characters/football/fb-017.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Xavi_Hernandez_2012.jpg/330px-Xavi_Hernandez_2012.jpg",
    "public/assets/characters/football/fb-022.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Kak%C3%A1_2010.jpg/330px-Kak%C3%A1_2010.jpg",
    "public/assets/characters/football/fb-023.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Zlatan_Ibrahimovi%C4%87_June_2018.jpg/330px-Zlatan_Ibrahimovi%C4%87_June_2018.jpg",
    "public/assets/characters/football/fb-024.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Sergio_Ramos_2018.jpg/330px-Sergio_Ramos_2018.jpg",
    "public/assets/characters/football/fb-026.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Toni_Kroos_2018.jpg/330px-Toni_Kroos_2018.jpg",
    "public/assets/characters/football/fb-028.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Vinicius_Junior_2018.jpg/330px-Vinicius_Junior_2018.jpg",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://en.wikipedia.org/"
}

for dest, url in DIRECT_URLS.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            with open(dest, "wb") as f:
                f.write(res.read())
        print(f"Downloaded {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"Error {dest}: {e}")
    time.sleep(0.3)

m_cnt = len([f for f in os.listdir("public/assets/characters/marvel") if f.endswith(".jpg")])
fb_cnt = len([f for f in os.listdir("public/assets/characters/football") if f.endswith(".jpg")])
print(f"DONE! Total Marvel: {m_cnt}/30, Total Football: {fb_cnt}/30")
