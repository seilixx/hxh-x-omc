import re

with open('src/data/hunter-x-hunter/characters.ts', 'r', encoding='utf-8') as f:
    text = f.read()

for cid in ['hxh-043', 'hxh-046', 'hxh-049']:
    m = re.search(r'id:\s*\'' + cid + r'\'[\s\S]*?hints:', text)
    if m:
        print(f"=== {cid} ===")
        print(m.group(0))

