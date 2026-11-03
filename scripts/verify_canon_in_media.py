import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_canon_in_media(media_id, char_name):
    query = """
    query ($mediaId: Int, $search: String) {
      Media(id: $mediaId) {
        characters(search: $search) {
          edges {
            role
            node {
              id
              name { full alternative }
              image { large }
            }
          }
        }
      }
    }
    """
    payload = json.dumps({'query': query, 'variables': {'mediaId': media_id, 'search': char_name}}).encode()
    req = urllib.request.Request(
        'https://graphql.anilist.co',
        data=payload,
        headers={'Content-Type': 'application/json', 'User-Agent': 'CanonVerifier/3.0'}
    )
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=8) as res:
                data = json.loads(res.read())
                edges = data['data']['Media']['characters']['edges']
                if edges:
                    n = edges[0]['node']
                    print(f"[FOUND] Media {media_id}: '{char_name}' -> ID {n['id']} ({n['name']['full']}): {n['image']['large']}")
                    return n
                else:
                    print(f"[NOT FOUND] Media {media_id}: '{char_name}'")
                    return None
        except Exception as e:
            time.sleep(1)
    return None

# Test on Naruto (Media 1735 / 20)
print("--- NARUTO ---")
find_canon_in_media(1735, "Danzou")
find_canon_in_media(1735, "A")
find_canon_in_media(1735, "Fourth Raikage")

# Test on One Piece (Media 21)
print("\n--- ONE PIECE ---")
find_canon_in_media(21, "Killer")
find_canon_in_media(21, "Roger")
find_canon_in_media(21, "Kinemon")
find_canon_in_media(21, "King")
find_canon_in_media(21, "Queen")

# Test on JJK (Media 113415 / 145064)
print("\n--- JJK ---")
find_canon_in_media(113415, "Junpei")
find_canon_in_media(113415, "Esou")
find_canon_in_media(113415, "Kechizu")
find_canon_in_media(145064, "Tengen")
find_canon_in_media(145064, "Ino")

