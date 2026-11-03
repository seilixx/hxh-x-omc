import urllib.request
import urllib.parse
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'HunterOMCQuiz/2.5 (https://example.com; ilies@hunteromc.dev)'
}

TITLES = [
    ('marvel-032.jpg', 'Magneto (Marvel Comics)'),
    ('marvel-036.jpg', 'Daredevil (Marvel Comics character)'),
    ('marvel-037.jpg', 'Punisher'),
    ('marvel-039.jpg', 'Ghost Rider'),
    ('marvel-041.jpg', 'Namor'),
    ('marvel-042.jpg', 'Ultron'),
    ('marvel-043.jpg', 'Hela (Marvel Comics)'),
    ('marvel-050.jpg', 'Emma Frost'),
]

for filename, title in TITLES:
    dest = os.path.join('public', 'assets', 'characters', 'marvel', filename)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as res:
                data = json.loads(res.read())
                img = data.get('thumbnail', {}).get('source') or data.get('originalimage', {}).get('source')
                if img:
                    img = img.split('?')[0]
                    img_req = urllib.request.Request(img, headers=headers)
                    with urllib.request.urlopen(img_req, timeout=12) as img_res:
                        content = img_res.read()
                        with open(dest, 'wb') as f:
                            f.write(content)
                    print(f"[OK] {filename} ({title}) -> {len(content)} bytes")
                    break
                else:
                    print(f"[NO IMG] {title}")
                    break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(3)
            else:
                print(f"[ERR] {title}: {e}")
                break
        except Exception as e:
            print(f"[ERR] {title}: {e}")
            break
    time.sleep(1)

print("Marvel missing download script done!")

