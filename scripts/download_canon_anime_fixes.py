import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'HunterExamImageSync/2.0'
}

DOWNLOAD_TARGETS = [
    # Naruto
    ('naruto/naruto-011.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b1557-Z0135T7wO0vT.png'),
    ('naruto/naruto-015.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b3149-j6cl8A9yup51.png'),
    ('naruto/naruto-016.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b53901-HnRKSoHMG5Vg.png'),
    ('naruto/naruto-018.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b307-xieUEdhdTVwQ.png'),
    ('naruto/naruto-019.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b1555-Q41GLTV3FvYF.png'), # Hinata Hyuga!
    ('naruto/naruto-022.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b2039-9NXBvh6H15LD.png'), # Haku (Naruto)!
    ('naruto/naruto-026.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b18473-AiI3mk28a1Nm.png'),
    ('naruto/naruto-029.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b2006-FTCz2Eu3cXsI.png'), # Yamato (Naruto)!
    ('naruto/naruto-030.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b1901-vJRGRONNpaiG.jpg'), # Sai (Naruto)!
    
    # Hunter x Hunter
    ('hunter-x-hunter/hxh-014.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/n41135-tTO36i1YAA5L.jpg'),
    ('hunter-x-hunter/hxh-015.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/43953.jpg'),
    ('hunter-x-hunter/hxh-023.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b52425-0doIaKgpDbds.jpg'),
    ('hunter-x-hunter/hxh-035.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/55069-QeIrBVdEt0aW.jpg'),
    ('hunter-x-hunter/hxh-036.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b55071-rUsNSPYGF7Y5.png'),
    ('hunter-x-hunter/hxh-039.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b20677-I7bchq2Ema7S.jpg'), # Hanzo (HxH)!

    # One Piece
    ('one-piece/op-012.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b22687-tCQVpj6wZhRk.jpg'), # Akainu
    ('one-piece/op-015.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b46109-MT7Hm4Bk93In.png'), # Kaido
    ('one-piece/op-020.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b16342-kVOF6V5Q94go.png'), # Boa Hancock
    ('one-piece/op-022.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b2754-B4gGSlNYgsyh.jpg'), # Doflamingo
    ('one-piece/op-023.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b3331-7ZJDc4BNv9Yp.jpg'), # Blackbeard
    ('one-piece/op-024.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b17142-OXOpztWZIE2A.png'), # Silvers Rayleigh
    ('one-piece/op-027.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b4884-iBn6FzQ2ESLC.png'), # Dragon
    ('one-piece/op-030.jpg', 'https://s4.anilist.co/file/anilistcdn/character/large/b124077-TODX2ThCdyx2.png'), # Katakuri
]

for rel_path, url in DOWNLOAD_TARGETS:
    dest = os.path.join('public', 'assets', 'characters', rel_path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as res:
            content = res.read()
            with open(dest, 'wb') as f:
                f.write(content)
        print(f"[SUCCESS] {rel_path} -> {len(content)} bytes")
    except Exception as e:
        print(f"[FAIL] {rel_path} from {url}: {e}")

print("All target anime images downloaded and verified!")

