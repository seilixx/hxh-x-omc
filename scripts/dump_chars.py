import re
import json

files = [
    ('hunter-x-hunter', 'src/data/hunter-x-hunter/characters.ts'),
    ('naruto', 'src/data/naruto/characters.ts'),
    ('jujutsu-kaisen', 'src/data/jujutsu-kaisen/characters.ts'),
    ('one-piece', 'src/data/one-piece/characters.ts'),
]

all_chars = {}
for folder, fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    pattern = r"id:\s*'([^']+)'[\s\S]*?name:\s*'([^']+)'[\s\S]*?image:\s*'([^']+)'"
    matches = re.findall(pattern, content)
    all_chars[folder] = [{'id': m[0], 'name': m[1], 'image': m[2]} for m in matches]

with open('scripts/all_characters.json', 'w', encoding='utf-8') as f:
    json.dump(all_chars, f, indent=2)

print("Exported characters to scripts/all_characters.json")
for folder in all_chars:
    print(f"{folder}: {len(all_chars[folder])} characters")
