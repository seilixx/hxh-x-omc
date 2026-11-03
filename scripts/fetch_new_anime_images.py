import urllib.request
import json
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/all_canon_characters.json', 'r', encoding='utf-8') as f:
    canon = json.load(f)

def search_anilist(term, anime_filter):
    query = """
    query ($search: String) {
      Page(page: 1, perPage: 6) {
        characters(search: $search) {
          id
          name { full alternative }
          media(type: ANIME, page: 1, perPage: 2) {
            nodes {
              title { romaji english }
            }
          }
          image { large }
        }
      }
    }
    """
    req = urllib.request.Request(
        'https://graphql.anilist.co',
        data=json.dumps({'query': query, 'variables': {'search': term}}).encode(),
        headers={'Content-Type': 'application/json', 'User-Agent': 'NewCharGetter/2.0'}
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=8) as res:
                data = json.loads(res.read())
                chars = data['data']['Page']['characters']
                for c in chars:
                    titles = ' '.join([m['title']['romaji'] + ' ' + (m['title']['english'] or '') for m in c['media']['nodes']]).lower()
                    if anime_filter.lower() in titles:
                        return c
                # if not matched with filter, return first if name is very specific
                if chars and term.lower() in chars[0]['name']['full'].lower():
                    return chars[0]
                return None
        except Exception as e:
            time.sleep(1.5)
    return None

NARUTO_NEW = [
    ("naruto-031", "Tobirama Senju", "Second Hokage"),
    ("naruto-032", "Hiruzen Sarutobi", "Third Hokage"),
    ("naruto-033", "Danzo Shimura", "Foundation"),
    ("naruto-034", "Hidan", "Akatsuki"),
    ("naruto-035", "Kakuzu", "Akatsuki"),
    ("naruto-036", "Konohamaru Sarutobi", "Genin"),
    ("naruto-037", "Shino Aburame", "Konoha"),
    ("naruto-038", "Kiba Inuzuka", "Konoha"),
    ("naruto-039", "Chouji Akimichi", "Konoha"),
    ("naruto-040", "Ino Yamanaka", "Konoha"),
    ("naruto-041", "Asuma Sarutobi", "Jonin"),
    ("naruto-042", "Kurenai Yuuhi", "Jonin"),
    ("naruto-043", "Kimimaro", "Sound Four"),
    ("naruto-044", "Kabuto Yakushi", "Sound"),
    ("naruto-045", "Mei Terumi", "Mizukage"),
    ("naruto-046", "Oonoki", "Tsuchikage"),
    ("naruto-047", "A", "Raikage"),
    ("naruto-048", "Mifune", "Samurai"),
    ("naruto-049", "Hagoromo Ootsutsuki", "Sage"),
    ("naruto-050", "Kaguya Ootsutsuki", "Goddess"),
]

JJK_NEW = [
    ("jjk-026", "Yuki Tsukumo", "Special Grade"),
    ("jjk-027", "Hajime Kashimo", "Culling Game"),
    ("jjk-028", "Hiromi Higuruma", "Lawyer"),
    ("jjk-029", "Kinji Hakari", "Jackpot"),
    ("jjk-030", "Kenjaku", "Curse User"),
    ("jjk-031", "Naoya Zenin", "Zenin Clan"),
    ("jjk-032", "Atsuya Kusakabe", "Simple Domain"),
    ("jjk-033", "Utahime Iori", "Kyoto High"),
    ("jjk-034", "Yoshinobu Gakuganji", "Principal"),
    ("jjk-035", "Momo Nishimiya", "Kyoto High"),
    ("jjk-036", "Junpei Yoshino", "Satozakura"),
    ("jjk-037", "Eso", "Death Painting"),
    ("jjk-038", "Kechizu", "Death Painting"),
    ("jjk-039", "Tengen", "Tomb of the Star"),
    ("jjk-040", "Takako Uro", "Sendai Colony"),
    ("jjk-041", "Ryuu Ishigoori", "Sendai Colony"),
    ("jjk-042", "Reggie Star", "Contract"),
    ("jjk-043", "Ui Ui", "Teleportation"),
    ("jjk-044", "Arata Nitta", "First Year"),
    ("jjk-045", "Shiu Kong", "Time Vessel"),
    ("jjk-046", "Miguel", "Curse User"),
    ("jjk-047", "Rika Orimoto", "Queen of Curses"),
    ("jjk-048", "Shouko Ieiri", "Doctor"),
    ("jjk-049", "Kiyotaka Ijichi", "Assistant Manager"),
    ("jjk-050", "Akari Nitta", "Assistant Manager"),
]

OP_NEW = [
    ("op-031", "Eustass Kid", "Captain"),
    ("op-032", "Killer", "Massacre Soldier"),
    ("op-033", "Jewelry Bonney", "Worst Generation"),
    ("op-034", "Basil Hawkins", "Magician"),
    ("op-035", "Bartholomew Kuma", "Tyrant"),
    ("op-036", "Gecko Moria", "Warlord"),
    ("op-037", "Enel", "God"),
    ("op-038", "Rob Lucci", "CP0"),
    ("op-039", "Kaku", "CP0"),
    ("op-040", "Borsalino", "Kizaru"),
    ("op-041", "Issho", "Fujitora"),
    ("op-042", "Sengoku", "Buddha"),
    ("op-043", "Gol D. Roger", "Pirate King"),
    ("op-044", "Kozuki Oden", "Samurai"),
    ("op-045", "Kozuki Momonosuke", "Shogun"),
    ("op-046", "Kin'emon", "Foxfire"),
    ("op-047", "Perona", "Ghost Princess"),
    ("op-048", "Caesar Clown", "Scientist"),
    ("op-049", "King", "Lunarian"),
    ("op-050", "Queen", "Scientist"),
]

results = {'naruto': {}, 'jjk': {}, 'op': {}}

print("Searching AniList for Naruto new characters...")
for cid, term, note in NARUTO_NEW:
    c = search_anilist(term, "naruto")
    if c:
        results['naruto'][cid] = {'name': c['name']['full'], 'img': c['image']['large'], 'term': term}
        print(f"  [OK] {cid} {term} -> {c['name']['full']}")
    else:
        print(f"  [MISS] {cid} {term}")
    time.sleep(0.35)

print("\nSearching AniList for JJK new characters...")
for cid, term, note in JJK_NEW:
    c = search_anilist(term, "jujutsu")
    if c:
        results['jjk'][cid] = {'name': c['name']['full'], 'img': c['image']['large'], 'term': term}
        print(f"  [OK] {cid} {term} -> {c['name']['full']}")
    else:
        print(f"  [MISS] {cid} {term}")
    time.sleep(0.35)

print("\nSearching AniList for One Piece new characters...")
for cid, term, note in OP_NEW:
    c = search_anilist(term, "one piece")
    if c:
        results['op'][cid] = {'name': c['name']['full'], 'img': c['image']['large'], 'term': term}
        print(f"  [OK] {cid} {term} -> {c['name']['full']}")
    else:
        print(f"  [MISS] {cid} {term}")
    time.sleep(0.35)

with open('scripts/new_anime_urls.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nSaved scripts/new_anime_urls.json!")

