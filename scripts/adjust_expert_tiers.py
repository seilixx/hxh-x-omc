import re

# Naruto
with open('src/data/naruto/characters.ts', 'r', encoding='utf-8') as f:
    n_text = f.read()

for cid in ['naruto-006', 'naruto-013', 'naruto-017']:
    n_text = re.sub(r'(id:\s*\'' + cid + r'\'[\s\S]*?difficulty:\s*\')\w+(\')', r'\g<1>expert\g<2>', n_text)

with open('src/data/naruto/characters.ts', 'w', encoding='utf-8') as f:
    f.write(n_text)

# One Piece
with open('src/data/one-piece/characters.ts', 'r', encoding='utf-8') as f:
    op_text = f.read()

for cid in ['op-011', 'op-024', 'op-042', 'op-044']:
    op_text = re.sub(r'(id:\s*\'' + cid + r'\'[\s\S]*?difficulty:\s*\')\w+(\')', r'\g<1>expert\g<2>', op_text)

with open('src/data/one-piece/characters.ts', 'w', encoding='utf-8') as f:
    f.write(op_text)

print("Adjusted expert tiers in Naruto and One Piece!")

