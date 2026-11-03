import fs from 'node:fs';

async function fetchSearch(search) {
  const res = await fetch('https://graphql.anilist.co', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: `query ($search: String) { Character(search: $search) { id name { full } image { large } } }`,
      variables: { search }
    })
  });
  const data = await res.json();
  console.log(search, '=>', data?.data?.Character);
  if (data?.data?.Character?.image?.large) {
    return data.data.Character.image.large;
  }
  return null;
}

async function run() {
  const kImg = await fetchSearch('Katakuri');
  if (kImg) {
    const res = await fetch(kImg);
    fs.writeFileSync('public/assets/characters/one-piece/op-030.jpg', Buffer.from(await res.arrayBuffer()));
    console.log('Saved Katakuri!');
  }

  const hImg = await fetchSearch('Hanami');
  if (hImg) {
    const res = await fetch(hImg);
    fs.writeFileSync('public/assets/characters/jujutsu-kaisen/jjk-014.jpg', Buffer.from(await res.arrayBuffer()));
    console.log('Saved Hanami!');
  }
}

run();
