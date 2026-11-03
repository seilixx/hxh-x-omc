import urllib.request
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'HunterExamApp/2.0'}

def get_anilist_media_characters(media_id, per_page=50):
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
    
    chars = []
    page = 1
    while page <= 2:
        payload = json.dumps({'query': query, 'variables': {'mediaId': media_id, 'page': page, 'perPage': per_page}}).encode()
        req = urllib.request.Request('https://graphql.anilist.co', data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'AntigravityApp'})
        try:
            with urllib.request.urlopen(req, timeout=10) as res:
                data = json.loads(res.read())
                char_data = data['data']['Media']['characters']
                edges = char_data['edges']
                chars.extend(edges)
                if not char_data['pageInfo']['hasNextPage']:
                    break
                page += 1
                time.sleep(1)
        except Exception as e:
            print(f"Error fetching media {media_id} page {page}: {e}")
            break
    return chars

# Let's test for Naruto (1735 is Shippuuden, 20 is Naruto)
print("Testing AniList Media characters query for Naruto Shippuuden (1735)...")
shippuuden_chars = get_anilist_media_characters(1735, per_page=25)
print(f"Retrieved {len(shippuuden_chars)} characters from Naruto Shippuuden.")
for c in shippuuden_chars[:10]:
    n = c['node']
    print(f"- {n['name']['full']} (ID: {n['id']}, Role: {c['role']}) -> {n['image']['large']}")

