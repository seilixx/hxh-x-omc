import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

MEDIA_MAP = {
    'hunter-x-hunter': [11061, 136],
    'naruto': [1735, 20],
    'jujutsu-kaisen': [113415, 145064, 105914],
    'one-piece': [21]
}

query = """
query ($mediaId: Int, $page: Int, $perPage: Int) {
  Media(id: $mediaId) {
    characters(page: $page, perPage: $perPage, sort: ROLE) {
      pageInfo {
        hasNextPage
      }
      edges {
        role
        node {
          id
          name {
            full
            native
            alternative
          }
          image {
            large
          }
        }
      }
    }
  }
}
"""

all_canon = {}

for universe, media_ids in MEDIA_MAP.items():
    print(f"\nFetching canon character directory for {universe}...")
    chars_by_name = {}
    for mid in media_ids:
        page = 1
        while page <= 3:
            payload = json.dumps({'query': query, 'variables': {'mediaId': mid, 'page': page, 'perPage': 50}}).encode()
            req = urllib.request.Request(
                'https://graphql.anilist.co',
                data=payload,
                headers={'Content-Type': 'application/json', 'User-Agent': 'HunterCharacterSync/2.0'}
            )
            try:
                with urllib.request.urlopen(req, timeout=10) as res:
                    data = json.loads(res.read())
                    edges = data['data']['Media']['characters']['edges']
                    for e in edges:
                        n = e['node']
                        cid = n['id']
                        full = n['name']['full']
                        img = n['image']['large']
                        alt = n['name']['alternative'] or []
                        # store by full name lowercase
                        chars_by_name[full.lower()] = {
                            'id': cid,
                            'full': full,
                            'img': img,
                            'alt': alt,
                            'role': e['role']
                        }
                    if not data['data']['Media']['characters']['pageInfo']['hasNextPage']:
                        break
                    page += 1
                    time.sleep(0.5)
            except Exception as ex:
                print(f"  Error fetching mid {mid} p{page}: {ex}")
                time.sleep(2)
                break
    all_canon[universe] = chars_by_name
    print(f"Found {len(chars_by_name)} unique canon characters for {universe}.")

with open('scripts/all_canon_characters.json', 'w', encoding='utf-8') as f:
    json.dump(all_canon, f, indent=2, ensure_ascii=False)

print("Saved scripts/all_canon_characters.json!")

