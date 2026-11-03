import re
import glob
import json
import urllib.request
import time

query = """
query ($search: String) {
  Character(search: $search) {
    id
    name {
      full
    }
    media(type: ANIME, page: 1, perPage: 3) {
      nodes {
        title {
          romaji
          english
        }
      }
    }
    image {
      large
    }
  }
}
"""

files = [
    ('hunter-x-hunter', 'src/data/hunter-x-hunter/characters.ts', 'Hunter x Hunter'),
    ('naruto', 'src/data/naruto/characters.ts', 'Naruto'),
    ('jujutsu-kaisen', 'src/data/jujutsu-kaisen/characters.ts', 'Jujutsu Kaisen'),
    ('one-piece', 'src/data/one-piece/characters.ts', 'One Piece'),
]

for folder, fpath, anime_title in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = r"id:\s*'([^']+)'[\s\S]*?name:\s*'([^']+)'"
    chars = re.findall(pattern, content)
    print(f"\nChecking {folder} ({len(chars)} characters)...")
    for cid, name in chars:
        # Check specific suspect characters first or list them
        pass
