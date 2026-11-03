import urllib.request
import json

def get_char(search):
    query = """
    query ($search: String) {
      Character(search: $search) {
        id
        name { full }
        image { large }
        media(page: 1, perPage: 1) { nodes { title { romaji } } }
      }
    }
    """
    req = urllib.request.Request('https://graphql.anilist.co', data=json.dumps({'query': query, 'variables': {'search': search}}).encode(), headers={'Content-Type': 'application/json', 'User-Agent': 'Test'})
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read())['data']['Character']
        print(search, "-> ID:", data['id'], data['name']['full'], "| Anime:", data['media']['nodes'][0]['title']['romaji'], "| Img:", data['image']['large'])

get_char("Knuckle Bine")
get_char("Knov")
get_char("Pakunoda")
