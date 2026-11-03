import urllib.request
import urllib.parse
import json

headers = {'User-Agent': 'HunterOMCQuiz/2.5 (https://example.com; ilies@hunteromc.dev)'}
url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote('Cyclops (Marvel Comics)')}"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as res:
    d = json.loads(res.read())
    img = d.get('thumbnail', {}).get('source').split('?')[0]
    ires = urllib.request.urlopen(urllib.request.Request(img, headers=headers))
    data = ires.read()
    with open('public/assets/characters/marvel/marvel-041.jpg', 'wb') as f:
        f.write(data)
    print('Saved Cyclops! Size:', len(data))

