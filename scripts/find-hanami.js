import fs from 'node:fs';

async function run() {
  const query = `
    query {
      Media(search: "Jujutsu Kaisen", type: ANIME) {
        characters(page: 2, perPage: 50) {
          nodes {
            id
            name { full native }
            image { large }
          }
        }
      }
    }
  `;
  const res = await fetch('https://graphql.anilist.co', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  const data = await res.json();
  const chars = data.data.Media.characters.nodes;
  const hanami = chars.find(c => c.name.full.toLowerCase().includes('hanami') || (c.name.native && c.name.native.includes('花御')));
  console.log('Hanami found on page 2:', hanami);
  if (hanami) {
    const imgRes = await fetch(hanami.image.large);
    fs.writeFileSync('public/assets/characters/jujutsu-kaisen/jjk-014.jpg', Buffer.from(await imgRes.arrayBuffer()));
    console.log('Saved JJK Hanami image!');
  } else {
    console.log('Sample names:', chars.slice(0, 10).map(c => c.name.full));
  }
}

run();
