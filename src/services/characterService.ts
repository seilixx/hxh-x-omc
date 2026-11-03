import type { Character, AnimeUniverse, Difficulty, GameConfig } from '../types';
import hxhCharacters from '../data/hunter-x-hunter/characters';
import narutoCharacters from '../data/naruto/characters';
import jjkCharacters from '../data/jujutsu-kaisen/characters';
import onePieceCharacters from '../data/one-piece/characters';
import marvelCharacters from '../data/marvel/characters';
import footballCharacters from '../data/football/characters';

const DATABASE: Record<AnimeUniverse, Character[]> = {
  'hunter-x-hunter': hxhCharacters,
  'naruto': narutoCharacters,
  'jujutsu-kaisen': jjkCharacters,
  'one-piece': onePieceCharacters,
  'marvel': marvelCharacters,
  'football': footballCharacters,
};

export function getCharacters(anime: AnimeUniverse): Character[] {
  return DATABASE[anime] ?? [];
}

export function filterCharacters(config: GameConfig): Character[] {
  let chars = getCharacters(config.anime);

  // Filter by difficulty
  if (config.difficulty && config.difficulty.length > 0) {
    chars = chars.filter(c => config.difficulty.includes(c.difficulty));
  }

  // Generic Arc filter with fuzzy arc matching
  if (config.arc && config.arc.length > 0) {
    chars = chars.filter(c => {
      if (!c.arc) return false;
      const cleanC = c.arc.replace(/\\/g, '').toLowerCase().trim();
      return config.arc!.some(a => {
        const cleanA = a.replace(/\\/g, '').toLowerCase().trim();
        return cleanC.includes(cleanA) || cleanA.includes(cleanC);
      });
    });
  }

  // Spoiler filter
  chars = chars.filter(c => (c.spoilerLevel ?? 0) <= config.spoilerLevel);

  // Anime-only filter
  if (!config.includeAnimeOnly) {
    chars = chars.filter(c => !c.isAnimeOnly);
  }

  // Manga-only filter
  if (!config.includeManga) {
    chars = chars.filter(c => !c.isMangaOnly);
  }

  // HxH specific filters
  if (config.anime === 'hunter-x-hunter') {
    if (config.hxhArc && config.hxhArc.length > 0) {
      chars = chars.filter(c => c.arc && config.hxhArc!.includes(c.arc));
    }
    if (config.hxhAffiliation && config.hxhAffiliation.length > 0) {
      chars = chars.filter(c => c.affiliation && config.hxhAffiliation!.some(a => c.affiliation!.includes(a)));
    }
    if (config.hxhNenType && config.hxhNenType.length > 0) {
      chars = chars.filter(c => c.nenType && config.hxhNenType!.some(n => c.nenType!.includes(n)));
    }
  }

  // Naruto specific filters
  if (config.anime === 'naruto') {
    if (config.narutoVillage && config.narutoVillage.length > 0) {
      chars = chars.filter(c => c.village && config.narutoVillage!.some(v => c.village!.includes(v)));
    }
    if (config.narutoClan && config.narutoClan.length > 0) {
      chars = chars.filter(c => c.clan && config.narutoClan!.some(cl => c.clan!.includes(cl)));
    }
  }

  // JJK specific filters
  if (config.anime === 'jujutsu-kaisen') {
    if (config.jjkSchool && config.jjkSchool.length > 0) {
      chars = chars.filter(c => c.school && config.jjkSchool!.some(s => c.school!.includes(s)));
    }
  }

  // One Piece specific filters
  if (config.anime === 'one-piece') {
    if (config.opCrew && config.opCrew.length > 0) {
      chars = chars.filter(c => c.crew && config.opCrew!.some(cr => c.crew!.includes(cr)));
    }
  }

  // Marvel specific filters
  if (config.anime === 'marvel') {
    if (config.marvelArc && config.marvelArc.length > 0) {
      chars = chars.filter(c => c.arc && config.marvelArc!.includes(c.arc));
    }
    if (config.marvelAffiliation && config.marvelAffiliation.length > 0) {
      chars = chars.filter(c => c.affiliation && config.marvelAffiliation!.some(a => c.affiliation!.includes(a)));
    }
  }

  // Football specific filters
  if (config.anime === 'football') {
    if (config.footballArc && config.footballArc.length > 0) {
      chars = chars.filter(c => c.arc && config.footballArc!.includes(c.arc));
    }
    if (config.footballAffiliation && config.footballAffiliation.length > 0) {
      chars = chars.filter(c => c.affiliation && config.footballAffiliation!.some(a => c.affiliation!.includes(a)));
    }
  }

  return chars;
}

export function getRandomFloat(): number {
  if (typeof window !== 'undefined' && window.crypto && window.crypto.getRandomValues) {
    const u32 = new Uint32Array(1);
    window.crypto.getRandomValues(u32);
    return u32[0] / (0xffffffff + 1);
  }
  return Math.random();
}

export function shuffleArray<T>(items: T[]): T[] {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(getRandomFloat() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

export function selectRandomCharacter(pool: Character[], excludeIds: string[] = []): Character | null {
  const available = pool.filter(c => !excludeIds.includes(c.id));
  if (available.length === 0) return null;
  const index = Math.floor(getRandomFloat() * available.length);
  return available[index];
}

export function getCharacterById(anime: AnimeUniverse, id: string): Character | undefined {
  return DATABASE[anime].find(c => c.id === id);
}

export function getDifficultyLabel(difficulty: Difficulty): string {
  const labels: Record<Difficulty, string> = {
    easy: 'EASY',
    medium: 'MEDIUM',
    hard: 'HARD',
    expert: 'EXPERT',
  };
  return labels[difficulty];
}
