import urllib.request
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0'}

DOWNLOADS = [
    # One Piece
    ('one-piece/op-032.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b2519-OfgRt6mP6Ae8.jpg'), # Kuro
    ('one-piece/op-043.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b4883-0t76xH00sehO.png'), # Gol D. Roger
    ('one-piece/op-046.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/n4875-Ga2TVjP70R6r.png'), # Bentham (Bon Clay)
    ('one-piece/op-049.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b4887-hMOqSSpR5jFc.jpg'), # Arlong
    ('one-piece/op-050.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b2753-Y2ja8Pl6PRs0.jpg'), # Smoker
    
    # Naruto
    ('naruto/naruto-033.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b3151-HDcp9mHbUvS7.png'), # Karin
    ('naruto/naruto-047.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/1903.jpg'), # Suigetsu
    
    # JJK
    ('jujutsu-kaisen/jjk-036.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b157214-ROBNoXVEXRNy.jpg'), # Junpei
    ('jujutsu-kaisen/jjk-037.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b210831-wsucHRbSZjbV.png'), # Esou
    ('jujutsu-kaisen/jjk-038.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b210832-d1Fg0CePSU86.png'), # Kechizu
    ('jujutsu-kaisen/jjk-039.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b217291-zKcyXtXLZZJy.png'), # Tengen
    ('jujutsu-kaisen/jjk-040.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b157865-X9ENX9OzWevS.jpg'), # Takuma Ino
    ('jujutsu-kaisen/jjk-041.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b189238-ItSLams6lRk9.png'), # Kiyotaka Ijichi
    ('jujutsu-kaisen/jjk-042.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b194056-yEzHVaAF9eqJ.png'), # Nagi Yoshino
    ('jujutsu-kaisen/jjk-043.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b194074-SnbrUkHIyM62.png'), # Wasuke Itadori
    ('jujutsu-kaisen/jjk-044.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b197119-Z2EBJXGTATzN.png'), # Takada-chan
    ('jujutsu-kaisen/jjk-045.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b200765-xQLkNIRUGuQw.jpg'), # Sasaki
    ('jujutsu-kaisen/jjk-046.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b200767-bTqPLS2Jpiqf.png'), # Iguchi
]

for rel_path, url in DOWNLOADS:
    dest = os.path.join('public', 'assets', 'characters', rel_path)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as res:
            content = res.read()
            with open(dest, 'wb') as f:
                f.write(content)
        print(f"[OK] {rel_path} -> {len(content)} bytes")
    except Exception as e:
        print(f"[ERR] {rel_path}: {e}")
    time.sleep(0.3)

print("Downloaded all remaining canon images!")

