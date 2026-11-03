import json
import os

with open("scripts/build_marvel_and_football.py", "r", encoding="utf-8") as f:
    code = f.read()

# Extract MARVEL_CHARACTERS and FOOTBALL_PLAYERS definitions
local_vars = {}
exec(code[:code.find("def fetch_wiki_image")], local_vars)

marvel = local_vars["MARVEL_CHARACTERS"]
football = local_vars["FOOTBALL_PLAYERS"]

for c in marvel:
    c["image"] = f"/assets/characters/marvel/{c['id']}.jpg"
    c["anime"] = "marvel"

for p in football:
    p["image"] = f"/assets/characters/football/{p['id']}.jpg"
    p["anime"] = "football"

with open("src/data/marvel/characters.ts", "w", encoding="utf-8") as f:
    f.write("import type { Character } from '../../types';\n\nexport const marvelCharacters: Character[] = " + json.dumps(marvel, indent=2) + ";\n\nexport default marvelCharacters;\n")
print(f"Generated src/data/marvel/characters.ts ({len(marvel)} characters)")

with open("src/data/football/characters.ts", "w", encoding="utf-8") as f:
    f.write("import type { Character } from '../../types';\n\nexport const footballCharacters: Character[] = " + json.dumps(football, indent=2) + ";\n\nexport default footballCharacters;\n")
print(f"Generated src/data/football/characters.ts ({len(football)} players)")
