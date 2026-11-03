import json

with open('scripts/all_canon_characters.json', 'r', encoding='utf-8') as f:
    canon = json.load(f)

for u in ['naruto', 'hunter-x-hunter', 'jujutsu-kaisen', 'one-piece']:
    print(f"\n=== {u.upper()} ===")
    names = list(canon[u].keys())
    for n in names[:35]:
        print(f"  {n}")

