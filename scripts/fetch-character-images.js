import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

const UNIVERSES = [
  { folder: 'hunter-x-hunter', file: 'src/data/hunter-x-hunter/characters.ts' },
  { folder: 'naruto', file: 'src/data/naruto/characters.ts' },
  { folder: 'jujutsu-kaisen', file: 'src/data/jujutsu-kaisen/characters.ts' },
  { folder: 'one-piece', file: 'src/data/one-piece/characters.ts' },
];

// Special name overrides for AniList search precision if needed
const SEARCH_OVERRIDES = {
  'Big Mom': 'Charlotte Linlin',
  'Pain': 'Pain',
  'Killer B': 'Killer B',
  'Toji Fushiguro': 'Toji Fushiguro',
  'Tony Tony Chopper': 'Tony Tony Chopper',
  'Edward Newgate': 'Edward Newgate',
  'Tserriednich Hui Guo Rou': 'Tserriednich',
  'Morena Prudo': 'Morena Prudo',
  'Bonolenov Ndongo': 'Bonolenov',
  'Phinks Magcub': 'Phinks',
  'Saiyu': 'Kanzai',
  'Kisho Arata': 'Arata Nitta',
};

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchFromAniList(searchName) {
  const query = `
    query ($search: String) {
      Character(search: $search) {
        id
        name {
          full
          native
        }
        image {
          large
          medium
        }
      }
    }
  `;

  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch('https://graphql.anilist.co', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          query,
          variables: { search: searchName }
        })
      });

      if (res.status === 429) {
        console.warn(`[429 Rate limit] Waiting 5 seconds before retry for "${searchName}"...`);
        await sleep(5000);
        continue;
      }

      if (!res.ok) {
        console.warn(`[AniList HTTP ${res.status}] for "${searchName}"`);
        return null;
      }

      const data = await res.json();
      return data?.data?.Character?.image?.large || data?.data?.Character?.image?.medium || null;
    } catch (err) {
      console.error(`Error querying AniList for "${searchName}":`, err.message);
      await sleep(1500);
    }
  }
  return null;
}

async function downloadImage(url, destPath) {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const res = await fetch(url);
      if (!res.ok) {
        console.warn(`Download failed HTTP ${res.status} for ${url}`);
        return false;
      }
      const arrayBuffer = await res.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);
      fs.writeFileSync(destPath, buffer);
      return true;
    } catch (err) {
      console.warn(`Download retry error for ${url}:`, err.message);
      await sleep(1500);
    }
  }
  return false;
}

async function main() {
  console.log('=== STARTING ANILIST CHARACTER IMAGE DOWNLOADER ===');

  for (const uni of UNIVERSES) {
    const fullPath = path.join(projectRoot, uni.file);
    if (!fs.existsSync(fullPath)) {
      console.warn(`File not found: ${fullPath}`);
      continue;
    }

    const outDir = path.join(projectRoot, 'public', 'assets', 'characters', uni.folder);
    if (!fs.existsSync(outDir)) {
      fs.mkdirSync(outDir, { recursive: true });
    }

    let content = fs.readFileSync(fullPath, 'utf8');

    // Regex match character blocks:
    // id: 'hxh-001',
    // name: 'Gon Freecss',
    const charRegex = /id:\s*'([^']+)',\s*\n\s*name:\s*'([^']+)'/g;
    let match;
    const characters = [];
    while ((match = charRegex.exec(content)) !== null) {
      characters.push({
        id: match[1],
        name: match[2],
      });
    }

    console.log(`\nFound ${characters.length} characters in ${uni.folder}`);

    let downloadedCount = 0;
    let alreadyExistsCount = 0;
    let fallbackCount = 0;

    for (let i = 0; i < characters.length; i++) {
      const char = characters[i];
      const targetImgPath = path.join(outDir, `${char.id}.jpg`);
      const publicPath = `/assets/characters/${uni.folder}/${char.id}.jpg`;

      if (fs.existsSync(targetImgPath) && fs.statSync(targetImgPath).size > 2000) {
        alreadyExistsCount++;
        continue;
      }

      const searchName = SEARCH_OVERRIDES[char.name] || char.name;
      process.stdout.write(`[${i + 1}/${characters.length}] Fetching ${char.name} (${searchName})... `);

      let imgUrl = await fetchFromAniList(searchName);
      if (!imgUrl && char.name.includes(' ')) {
        // try first word (e.g. "Chrollo" for "Chrollo Lucilfer")
        const firstWord = char.name.split(' ')[0];
        imgUrl = await fetchFromAniList(firstWord);
      }

      if (imgUrl) {
        const ok = await downloadImage(imgUrl, targetImgPath);
        if (ok) {
          const sizeKb = Math.round(fs.statSync(targetImgPath).size / 1024);
          console.log(`Saved (${sizeKb} KB)`);
          downloadedCount++;
        } else {
          console.log(`Download failed!`);
          fallbackCount++;
        }
      } else {
        console.log(`Not found on AniList!`);
        fallbackCount++;
      }

      // Small pacing to avoid aggressive bursts
      await sleep(350);
    }

    console.log(`Finished ${uni.folder}: ${downloadedCount} downloaded, ${alreadyExistsCount} already existed, ${fallbackCount} failed/fallback.`);

    // Now update the characters.ts file so image: points to /assets/characters/<folder>/<id>.jpg
    // Find:
    // id: 'hxh-001',
    // ...
    // image: '...',
    // Replace that image with /assets/characters/<folder>/<id>.jpg
    // Let's do a reliable replacement using block matching
    let updatedContent = content;
    for (const char of characters) {
      const targetImgPath = path.join(outDir, `${char.id}.jpg`);
      if (fs.existsSync(targetImgPath) && fs.statSync(targetImgPath).size > 2000) {
        // Replace image: '...' in this character's block
        const escapedId = char.id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        // Match from id: 'char.id' up to image: '...'
        const regex = new RegExp(`(id:\\s*'${escapedId}'[\\s\\S]*?image:\\s*')[^']+(')`, 'g');
        updatedContent = updatedContent.replace(regex, `$1/assets/characters/${uni.folder}/${char.id}.jpg$2`);
      }
    }

    if (updatedContent !== content) {
      fs.writeFileSync(fullPath, updatedContent, 'utf8');
      console.log(`Updated ${uni.file} with local image URLs.`);
    }
  }

  console.log('\n=== ALL UNIVERSES PROCESSED SUCCESSFULLY ===\n');
}

main().catch(err => {
  console.error('Fatal error in downloader:', err);
  process.exit(1);
});
