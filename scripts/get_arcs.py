import re

for anime, path in [
    ('HxH', 'src/data/hunter-x-hunter/characters.ts'),
    ('Naruto', 'src/data/naruto/characters.ts'),
    ('JJK', 'src/data/jujutsu-kaisen/characters.ts'),
    ('One Piece', 'src/data/one-piece/characters.ts'),
    ('Marvel', 'src/data/marvel/characters.ts'),
    ('Football', 'src/data/football/characters.ts'),
]:
    content = open(path, encoding='utf-8').read()
    arcs = sorted(set(re.findall(r'arc[\'"]?:\s*[\'"]([^\'"]+)[\'"]', content)))
    print(f"{anime} arcs: {arcs}")
