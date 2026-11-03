import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_char_by_name(search_term, anime_keyword):
    query = """
    query ($search: String) {
      Page(page: 1, perPage: 10) {
        characters(search: $search) {
          id
          name {
            full
            native
          }
          media(type: ANIME, page: 1, perPage: 3) {
            nodes {
              id
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
    }
    """
    payload = json.dumps({'query': query, 'variables': {'search': search_term}}).encode()
    req = urllib.request.Request('https://graphql.anilist.co', data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'TestCharFinder'})
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read())
            chars = data['data']['Page']['characters']
            for c in chars:
                titles = []
                for m in c['media']['nodes']:
                    t = m['title']
                    titles.append((t.get('romaji') or '') + ' ' + (t.get('english') or ''))
                combined = ' '.join(titles).lower()
                if anime_keyword.lower() in combined:
                    print(f"FOUND: '{search_term}' -> ID {c['id']} ({c['name']['full']}) in {[m['title']['romaji'] for m in c['media']['nodes']]}")
                    print(f"  Image: {c['image']['large']}")
                    return c
            print(f"NOT FOUND for '{search_term}' in '{anime_keyword}'")
    except Exception as e:
        print(f"Error for '{search_term}': {e}")
    return None

test_list = [
    ("Boa Hancock", "One Piece"),
    ("Silvers Rayleigh", "One Piece"),
    ("Kaido", "One Piece"),
    ("Charlotte Katakuri", "One Piece"),
    ("Sakazuki", "One Piece"),
    ("Madara Uchiha", "Naruto"),
    ("Obito Uchiha", "Naruto"),
    ("Killer B", "Naruto"),
    ("Shaiapouf", "Hunter"),
    ("Menthuthuyoupi", "Hunter"),
    ("Alluka Zoldyck", "Hunter"),
    ("Pariston Hill", "Hunter"),
    ("Cheadle Yorkshire", "Hunter"),
]

for name, kw in test_list:
    find_char_by_name(name, kw)

