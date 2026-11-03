import urllib.request
import json

query = """
query ($mediaId: Int) {
  Media(id: $mediaId) {
    title { romaji }
    characters(page: 1, perPage: 10) {
      nodes {
        id
        name { full }
        image { large }
      }
    }
  }
}
"""

req = urllib.request.Request(
    'https://graphql.anilist.co',
    data=json.dumps({'query': query, 'variables': {'mediaId': 11061}}).encode(),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Test'}
)
with urllib.request.urlopen(req) as res:
    d = json.loads(res.read())['data']['Media']
    print(d['title']['romaji'])
    for c in d['characters']['nodes']:
        print(f"  {c['name']['full']} -> {c['image']['large']}")
