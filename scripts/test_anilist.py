import urllib.request
import json

query = """
query ($search: String) {
  Character(search: $search) {
    id
    name { full }
    media(type: ANIME, page: 1, perPage: 1) {
      nodes { title { romaji english } }
    }
    image { large }
  }
}
"""

def check(name):
    req = urllib.request.Request(
        'https://graphql.anilist.co',
        data=json.dumps({'query': query, 'variables': {'search': name}}).encode(),
        headers={'Content-Type': 'application/json', 'User-Agent': 'Test'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            d = json.loads(res.read())['data']['Character']
            title = d['media']['nodes'][0]['title']['romaji'] if d['media']['nodes'] else 'None'
            print(f"{name} -> {d['name']['full']} (Anime: {title})")
    except Exception as e:
        print(f"{name} -> Error {e}")

for n in ['Saiyu', 'Bonolenov Ndongo', 'Phinks Magcub', 'Morena Prudo', 'Tserriednich', 'Knuckle', 'Pakunoda', 'Knov', 'Alluka Zoldyck', 'Nanika']:
    check(n)
