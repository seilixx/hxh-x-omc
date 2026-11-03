import urllib.request
import json

query = """
query {
  Character(search: "Touji Fushiguro") {
    id
    name { full }
    image { large }
    media(page: 1, perPage: 1) { nodes { title { romaji } } }
  }
}
"""
req = urllib.request.Request('https://graphql.anilist.co', data=json.dumps({'query': query}).encode(), headers={'Content-Type': 'application/json', 'User-Agent': 'Test'})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read())['data']['Character']
    print(data['id'], data['name']['full'], data['media']['nodes'][0]['title']['romaji'], data['image']['large'])
