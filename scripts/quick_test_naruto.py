import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_query(search):
    q = """
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
        data=json.dumps({'query': q, 'variables': {'search': search}}).encode(),
        headers={'Content-Type': 'application/json', 'User-Agent': 'TestAuditor'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            d = json.loads(res.read())['data']['Character']
            print(f"'{search}': ID={d['id']} full='{d['name']['full']}' anime='{[m['title']['romaji'] for m in d['media']['nodes']]}'")
    except Exception as e:
        print(f"'{search}': error {e}")

test_query("Hinata Hyuuga")
test_query("Hinata Hyuga")
test_query("Pain / Nagato")
test_query("Killer Bee")
test_query("Might Guy")
test_query("Zabuza Momochi")

