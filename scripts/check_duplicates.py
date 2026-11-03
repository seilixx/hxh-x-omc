import json

with open('scripts/all_characters.json') as f:
    data = json.load(f)

for universe, chars in data.items():
    print(f"=== {universe} ===")
    seen = {}
    for c in chars:
        name = c['name'].lower()
        if name in seen:
            print(f"Duplicate name: '{c['name']}' (IDs: {seen[name]}, {c['id']})")
        seen[name] = c['id']

    # check aliases or accepted answers overlaps
