import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const REMAINING = [
  // HxH
  { id: 'hxh-031', name: 'Pakunoda', search: 'Pakunoda', folder: 'hunter-x-hunter', anilistId: 168 },
  { id: 'hxh-044', name: 'Knov', search: 'Knov', folder: 'hunter-x-hunter', anilistId: 5092 },
  { id: 'hxh-045', name: 'Knuckle', search: 'Knuckle Bine', folder: 'hunter-x-hunter', anilistId: 5090 },
  { id: 'hxh-047', name: 'Killua', search: 'Killua Zoldyck', folder: 'hunter-x-hunter', anilistId: 27 },

  // Naruto
  { id: 'naruto-021', name: 'Zabuza Momochi', search: 'Zabuza Momochi', folder: 'naruto', anilistId: 412 },

  // JJK
  { id: 'jjk-013', name: 'Maki Zenin', search: "Maki Zen'in", folder: 'jujutsu-kaisen', anilistId: 133701 },
  { id: 'jjk-014', name: 'Hanami', search: 'Hanami', folder: 'jujutsu-kaisen', anilistId: 133706 },

  // One Piece
  { id: 'op-020', name: 'Boa Hancock', search: 'Hancock Boa', folder: 'one-piece', anilistId: 18938 },
  { id: 'op-029', name: 'Buggy', search: 'Buggy', folder: 'one-piece', anilistId: 2146 },
  { id: 'op-030', name: 'Charlotte Katakuri', search: 'Charlotte Katakuri', folder: 'one-piece', anilistId: 125134 },
];

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchAniListByIdOrSearch(item) {
  const query = `
    query ($id: Int, $search: String) {
      Character(id: $id, search: $search) {
        id
        name { full }
        image { large medium }
      }
    }
  `;

  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch('https://graphql.anilist.co', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          variables: item.anilistId ? { id: item.anilistId } : { search: item.search }
        })
      });

      if (res.status === 429) {
        console.warn(`[429 Rate limit] Waiting 15s for ${item.name}...`);
        await sleep(15000);
        continue;
      }

      if (!res.ok) {
        console.warn(`HTTP ${res.status} for ${item.name}`);
        return null;
      }

      const data = await res.json();
      return data?.data?.Character?.image?.large || data?.data?.Character?.image?.medium || null;
    } catch (err) {
      console.warn(`Err: ${err.message}`);
      await sleep(2000);
    }
  }
  return null;
}

async function download(url, dest) {
  try {
    const res = await fetch(url);
    if (!res.ok) return false;
    const buf = Buffer.from(await res.arrayBuffer());
    fs.writeFileSync(dest, buf);
    return true;
  } catch (err) {
    return false;
  }
}

async function main() {
  console.log('=== FETCHING REMAINING CHARACTERS ===');

  for (const item of REMAINING) {
    const outDir = path.join(projectRoot, 'public', 'assets', 'characters', item.folder);
    const dest = path.join(outDir, `${item.id}.jpg`);

    if (fs.existsSync(dest) && fs.statSync(dest).size > 2000) {
      console.log(`Already exists: ${item.name}`);
      continue;
    }

    process.stdout.write(`Fetching ${item.name}... `);
    const url = await fetchAniListByIdOrSearch(item);
    if (url) {
      const ok = await download(url, dest);
      if (ok) {
        const kb = Math.round(fs.statSync(dest).size / 1024);
        console.log(`SAVED (${kb} KB)`);
      } else {
        console.log('Download failed');
      }
    } else {
      console.log('Not found');
    }
    await sleep(1200);
  }

  // Update file links for these remaining characters
  for (const item of REMAINING) {
    const targetFile = path.join(projectRoot, 'src', 'data', item.folder, 'characters.ts');
    if (!fs.existsSync(targetFile)) continue;
    let content = fs.readFileSync(targetFile, 'utf8');
    const regex = new RegExp(`(id:\\s*'${item.id}'[\\s\\S]*?image:\\s*')[^']+(')`, 'g');
    const updated = content.replace(regex, `$1/assets/characters/${item.folder}/${item.id}.jpg$2`);
    if (updated !== content) {
      fs.writeFileSync(targetFile, updated, 'utf8');
      console.log(`Updated link for ${item.name} in ${item.folder}`);
    }
  }

  console.log('Done!');
}

main();
