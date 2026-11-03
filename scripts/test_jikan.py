import urllib.request
import json
import urllib.parse

def test_jikan(name):
    url = f"https://api.jikan.moe/v4/characters?q={urllib.parse.quote(name)}&limit=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            d = json.loads(res.read())
            if d['data']:
                c = d['data'][0]
                img = c['images']['jpg']['image_url']
                print(f"{name} -> Jikan: {c['name']} | {img}")
    except Exception as e:
        print(f"{name} -> Error {e}")

test_jikan("Knuckle Bine")
test_jikan("Saiyu")
