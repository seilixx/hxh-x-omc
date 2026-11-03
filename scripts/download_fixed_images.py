import urllib.request
import json
import os

CHARACTERS_TO_UPDATE = [
    {
        "id": "jjk-024",
        "folder": "jujutsu-kaisen",
        "anilist_id": 138096, # Toji Fushiguro
        "name": "Toji Fushiguro"
    },
    {
        "id": "jjk-025",
        "folder": "jujutsu-kaisen",
        "anilist_id": 133705, # Jogo
        "name": "Jogo"
    },
    {
        "id": "op-023",
        "folder": "one-piece",
        "anilist_id": 2149, # Blackbeard
        "name": "Marshall D. Teach"
    },
    {
        "id": "op-024",
        "folder": "one-piece",
        "anilist_id": 18939, # Silvers Rayleigh
        "name": "Silvers Rayleigh"
    },
    {
        "id": "hxh-045",
        "folder": "hunter-x-hunter",
        "anilist_id": 5084, # Genthru
        "name": "Genthru"
    },
    {
        "id": "hxh-047",
        "folder": "hunter-x-hunter",
        "anilist_id": 5088, # Meleoron
        "name": "Meleoron"
    },
    {
        "id": "hxh-017",
        "folder": "hunter-x-hunter",
        "anilist_id": 5090, # Knuckle Bine
        "name": "Knuckle Bine"
    },
    {
        "id": "hxh-044",
        "folder": "hunter-x-hunter",
        "anilist_id": 5092, # Knov
        "name": "Knov"
    }
]

query = """
query ($id: Int) {
  Character(id: $id) {
    id
    name { full }
    image { large }
  }
}
"""

for item in CHARACTERS_TO_UPDATE:
    body = json.dumps({"query": query, "variables": {"id": item["anilist_id"]}}).encode()
    req = urllib.request.Request(
        "https://graphql.anilist.co",
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "Antigravity"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read())
            c = data["data"]["Character"]
            img_url = c["image"]["large"]
            dest = f"public/assets/characters/{item['folder']}/{item['id']}.jpg"
            print(f"Downloading {item['name']} ({c['name']['full']}) from {img_url} to {dest}...")
            img_req = urllib.request.Request(img_url, headers={"User-Agent": "Antigravity"})
            with urllib.request.urlopen(img_req, timeout=10) as img_res:
                with open(dest, "wb") as out_file:
                    out_file.write(img_res.read())
            print(f"  Saved {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"Error {item['name']}: {e}")

print("Done updating target character images!")
