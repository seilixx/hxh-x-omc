import json

with open('src/data/marvel/characters.ts', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = 'export const marvelCharacters: Character[] = '
data = json.loads(text[text.find(prefix) + len(prefix):text.rfind(';')])

for c in data[18:]:
    print(c['id'], c['name'])

