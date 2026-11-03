// ============================================================
// CORE TYPE DEFINITIONS
// ============================================================

export type AnimeUniverse =
  | 'hunter-x-hunter'
  | 'naruto'
  | 'jujutsu-kaisen'
  | 'one-piece'
  | 'marvel'
  | 'football';

export type LeaderboardCategory = AnimeUniverse | 'movies';
export type Difficulty = 'easy' | 'medium' | 'hard' | 'expert';
export type GameMode = 'classic' | 'time-attack' | 'endless';
export type GameStatus = 'idle' | 'playing' | 'correct' | 'timeout' | 'result';

export interface CharacterHint {
  time: 0 | 30 | 60 | 90; // seconds at which hint is revealed
  text: string;
}

export interface Character {
  id: string;
  name: string;
  acceptedAnswers: string[]; // all valid answers including name, aliases, alternate spellings
  aliases: string[];
  image: string; // URL or path
  anime: AnimeUniverse;
  arc?: string;
  affiliation?: string;
  description: string;
  difficulty: Difficulty;
  hints: CharacterHint[];
  // HxH specific
  nenType?: string;
  abilities?: string[];
  // Naruto specific
  village?: string;
  clan?: string;
  rank?: string;
  // JJK specific
  school?: string;
  grade?: string;
  cursedTechnique?: string;
  // One Piece specific
  crew?: string;
  devilFruit?: string;
  bounty?: string;
  haki?: string[];
  // Marvel / Football specific
  role?: string;
  team?: string;
  nationality?: string;
  // Metadata
  wiki?: string;
  isAnimeOnly?: boolean;
  isMangaOnly?: boolean;
  spoilerLevel?: number; // 0 = safe, 1 = mild, 2 = major
  family?: string[];
}

export interface GameConfig {
  anime: AnimeUniverse;
  mode: GameMode;
  difficulty: Difficulty[];
  rounds: number;
  includeAnimeOnly: boolean;
  includeManga: boolean;
  spoilerLevel: number;
  // Generic arc filter for any universe
  arc?: string[];
  // HxH filters
  hxhArc?: string[];
  hxhAffiliation?: string[];
  hxhNenType?: string[];
  // Naruto filters
  narutoVillage?: string[];
  narutoClan?: string[];
  // JJK filters
  jjkSchool?: string[];
  jjkType?: 'sorcerer' | 'curse' | 'both';
  // OP filters
  opCrew?: string[];
  opAffiliation?: string[];
  // Marvel filters
  marvelArc?: string[];
  marvelAffiliation?: string[];
  // Football filters
  footballArc?: string[];
  footballAffiliation?: string[];
}

export interface RoundResult {
  character: Character;
  isCorrect: boolean;
  timeElapsed: number; // seconds
  hintsRevealed: number;
  pointsEarned: number;
  guess?: string;
}

export interface GameSession {
  id: string;
  anime: AnimeUniverse;
  mode: GameMode;
  difficulty: Difficulty[];
  rounds: RoundResult[];
  totalScore: number;
  startedAt: number;
  completedAt?: number;
}

export interface LeaderboardEntry {
  id: string;
  nickname: string;
  anime: LeaderboardCategory;
  mode: GameMode;
  totalScore: number;
  correctGuesses: number;
  totalRounds: number;
  bestTime: number; // fastest correct answer in seconds
  date: string;
}

export interface GameState {
  status: GameStatus;
  config: GameConfig;
  session: GameSession | null;
  currentRound: number;
  currentCharacter: Character | null;
  elapsedTime: number; // seconds
  hintsRevealed: number;
  guess: string;
  lastResult: RoundResult | null;
}

export const SCORING_TABLE: { max: number; points: number }[] = [
  { max: 30, points: 100 },
  { max: 60, points: 80 },
  { max: 90, points: 60 },
  { max: 120, points: 40 },
];

export const HINT_TIMES = [30, 60, 90] as const;
export const ROUND_DURATION = 120; // seconds

export const BLUR_STAGES = [
  { time: 0, blur: 28 },
  { time: 30, blur: 28 },
  { time: 60, blur: 14 },
  { time: 90, blur: 6 },
  { time: 120, blur: 0 },
] as const;

export const ANIME_META: Record<AnimeUniverse, {
  label: string;
  shortLabel: string;
  tagline: string;
  description: string;
  accent: string;
  glow: string;
  theme: string;
  examLabel: string;
}> = {
  'hunter-x-hunter': {
    label: 'Hunter x Hunter',
    shortLabel: 'HxH',
    tagline: 'MAIN EXAM',
    description: 'Enter the Hunter Association universe. Face characters from the Hunter Exam to the Dark Continent.',
    accent: '#4ADE80',
    glow: 'rgba(74, 222, 128, 0.2)',
    theme: 'hxh',
    examLabel: 'HUNTER ASSOCIATION EXAM',
  },
  naruto: {
    label: 'Naruto',
    shortLabel: 'Naruto',
    tagline: 'SHINOBI EXAM',
    description: 'Prove your knowledge of the shinobi world. From Konoha to Akatsuki, every ninja awaits.',
    accent: '#F97316',
    glow: 'rgba(249, 115, 22, 0.2)',
    theme: 'naruto',
    examLabel: 'CHUNIN SELECTION EXAM',
  },
  'jujutsu-kaisen': {
    label: 'Jujutsu Kaisen',
    shortLabel: 'JJK',
    tagline: 'SORCERER EXAM',
    description: 'Enter the world of cursed energy. Identify sorcerers, curses, and everything between.',
    accent: '#A855F7',
    glow: 'rgba(168, 85, 247, 0.2)',
    theme: 'jjk',
    examLabel: 'JUJUTSU HIGH SELECTION',
  },
  'one-piece': {
    label: 'One Piece',
    shortLabel: 'OP',
    tagline: 'GRAND LINE EXAM',
    description: 'Sail the Grand Line and prove your pirate knowledge. From East Blue to the New World.',
    accent: '#EAB308',
    glow: 'rgba(234, 179, 8, 0.2)',
    theme: 'op',
    examLabel: 'GRAND LINE NAVIGATION EXAM',
  },
  marvel: {
    label: 'Marvel Universe',
    shortLabel: 'Marvel',
    tagline: 'MULTIVERSE EXAM',
    description: 'Earth-616 to cosmic realms. Earth\'s mightiest heroes, mutants, galactic rogues and cosmic titans.',
    accent: '#EF4444',
    glow: 'rgba(239, 68, 68, 0.25)',
    theme: 'marvel',
    examLabel: 'S.H.I.E.L.D. AVENGERS INITIATIVE',
  },
  football: {
    label: 'World Football',
    shortLabel: 'Football',
    tagline: 'BALLON D\'OR EXAM',
    description: 'Legends of the beautiful game. World Cup champions, UEFA icons, record breakers and maestros.',
    accent: '#10B981',
    glow: 'rgba(16, 185, 129, 0.25)',
    theme: 'football',
    examLabel: 'GOLDEN BALL LEGENDS TRIAL',
  },
};

