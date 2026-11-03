import urllib.request
import urllib.parse
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://en.wikipedia.org/'
}

DIRECT_WIKI = [
    ('football/fb-045.jpg', 'https://upload.wikimedia.org/wikipedia/commons/7/75/Dennis_Bergkamp_2014_%28cropped%29.jpg'),
    ('marvel/marvel-031.jpg', 'https://upload.wikimedia.org/wikipedia/en/e/e1/Doctor_Doom_%28circa_2019%29.png'),
    ('marvel/marvel-032.jpg', 'https://upload.wikimedia.org/wikipedia/en/7/77/Magneto_%28circa_2019%29.png'),
    ('marvel/marvel-033.jpg', 'https://upload.wikimedia.org/wikipedia/en/a/a7/Galactus_%282018%29.jpg'),
    ('marvel/marvel-034.jpg', 'https://upload.wikimedia.org/wikipedia/en/3/34/Silver_Surfer.png'),
    ('marvel/marvel-036.jpg', 'https://upload.wikimedia.org/wikipedia/en/3/3a/Daredevil_%28circa_2019%29.png'),
    ('marvel/marvel-037.jpg', 'https://upload.wikimedia.org/wikipedia/en/c/c8/Punisher_%28circa_2026%29.png'),
    ('marvel/marvel-038.jpg', 'https://upload.wikimedia.org/wikipedia/en/3/37/Blade_%28Marvel_Comics%29.png'),
    ('marvel/marvel-039.jpg', 'https://upload.wikimedia.org/wikipedia/en/1/1f/GhostRiderCVR001b.jpg'),
    ('marvel/marvel-040.jpg', 'https://upload.wikimedia.org/wikipedia/en/4/4a/Moon_Knight_%28Marc_Spector%29.png'),
    ('marvel/marvel-041.jpg', 'https://upload.wikimedia.org/wikipedia/en/1/1e/Namor_%28circa_2019%29.png'),
    ('marvel/marvel-042.jpg', 'https://upload.wikimedia.org/wikipedia/en/8/89/Ultron_%28circa_2018%29.png'),
    ('marvel/marvel-043.jpg', 'https://upload.wikimedia.org/wikipedia/en/d/db/Hela.png'),
    ('marvel/marvel-044.jpg', 'https://upload.wikimedia.org/wikipedia/en/f/fd/Guardians-17.jpg'),
    ('marvel/marvel-050.jpg', 'https://upload.wikimedia.org/wikipedia/en/0/02/Emma_Frost_%28Modern%29.webp'),
]

for rel_path, url in DIRECT_WIKI:
    dest = os.path.join('public', 'assets', 'characters', rel_path)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as res:
            content = res.read()
            with open(dest, 'wb') as f:
                f.write(content)
        print(f"[OK] {rel_path} -> {len(content)} bytes")
    except Exception as e:
        print(f"[FAIL] {rel_path}: {e}")
    time.sleep(0.5)

print("Direct wiki downloads complete!")

