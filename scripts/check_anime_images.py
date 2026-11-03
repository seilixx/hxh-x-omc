import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

query = """
query ($search: String) {
  Character(search: $search) {
    id
    name { full native }
    media(type: ANIME, page: 1, perPage: 2) {
      nodes {
        title { romaji english }
      }
    }
    image { large }
  }
}
"""

req = urllib.request.Request(
    'https://graphql.anilist.co',
    data=json.dumps({'query': query, 'variables': {'search': 'Hinata'}}).encode(),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Antigravity'}
)
with urllib.request.urlopen(req) as res:
    d = json.loads(res.read())['data']['Character']
    print("Search 'Hinata':")
    print("Name:", d['name'])
    print("Media:", [m['title'] for m in d['media']['nodes']])
    print("Image:", d['image'])
