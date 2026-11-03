import re

def check_file(path, ids):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    for cid in ids:
        m = re.search(r'id[\'"]?\s*:\s*[\'"]' + cid + r'[\'"][\s\S]*?name[\'"]?\s*:\s*[\'"]([^\'"]+)', text)
        if m:
            print(f'{cid}: {m.group(1)}')

print('--- HxH ---')
check_file('src/data/hunter-x-hunter/characters.ts', ['hxh-001', 'hxh-046', 'hxh-002', 'hxh-049', 'hxh-003', 'hxh-043'])
print('--- One Piece ---')
check_file('src/data/one-piece/characters.ts', ['op-001', 'op-027', 'op-010', 'op-020'])
print('--- Marvel ---')
check_file('src/data/marvel/characters.ts', ['marvel-001', 'marvel-002', 'marvel-011', 'marvel-021'])

