import json
import urllib.request
import time

query = """
query ($search: String) {
  Character(search: $search) {
    id
    name { full native }
    media(type: ANIME, page: 1, perPage: 3) {
      nodes {
        id
        title { romaji english }
      }
    }
    image { large }
  }
}
"""

with open('scripts/all_characters.json', 'r', encoding='utf-8') as f:
    all_data = json.load(f)

expected_keywords = {
    'hunter-x-hunter': ['hunter', 'hxh'],
    'naruto': ['naruto', 'boruto'],
    'jujutsu-kaisen': ['jujutsu'],
    'one-piece': ['one piece'],
}

mismatches = []

def test_character(folder, cid, name):
    body = json.dumps({'query': query, 'variables': {'search': name}}).encode()
    req = urllib.request.Request(
        'https://graphql.anilist.co',
        data=body,
        headers={'Content-Type': 'application/json', 'User-Agent': 'Antigravity'}
    )
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read())
                c = data.get('data', {}).get('Character')
                if not c:
                    print(f"[{folder}] {cid} {name} -> NOT FOUND")
                    mismatches.append((folder, cid, name, "Not found on AniList"))
                    return
                # Check media
                titles = []
                for m in c.get('media', {}).get('nodes', []):
                    t = m.get('title', {})
                    titles.append((t.get('romaji') or '') + ' ' + (t.get('english') or ''))
                combined_titles = ' '.join(titles).lower()
                
                kw_match = any(kw in combined_titles for kw in expected_keywords[folder])
                if not kw_match:
                    print(f"[{folder}] MISMATCH: {cid} '{name}' -> AniList returned '{c['name']['full']}' from '{titles[:2]}'")
                    mismatches.append((folder, cid, name, f"AniList returned {c['name']['full']} from {titles[:2]}"))
                else:
                    # Match is fine
                    pass
                return
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(3)
                continue
            print(f"HTTP {e.code} for {name}")
            return
        except Exception as e:
            print(f"Error {name}: {e}")
            return

print("Checking character anime associations on AniList...")
count = 0
for folder, chars in all_data.items():
    for c in chars:
        test_character(folder, c['id'], c['name'])
        count += 1
        time.sleep(0.4)
        if count % 20 == 0:
            print(f"Processed {count} characters...")

print("\n--- SUMMARY OF MISMATCHES ---")
for m in mismatches:
    print(m)

with open('scripts/mismatches.json', 'w') as f:
    json.dump(mismatches, f, indent=2)
