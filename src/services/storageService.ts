import type { LeaderboardEntry, GameSession, RoundResult, GameMode } from '../types';

const LEADERBOARD_KEY = 'omc_leaderboard';
const PREFS_KEY = 'omc_prefs';

export const DEFAULT_LEADERBOARD_ENTRIES: LeaderboardEntry[] = [
  {
    id: 'seed-01',
    nickname: 'Killua Zoldyck',
    anime: 'hunter-x-hunter',
    mode: 'time-attack',
    totalScore: 500,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 6.8,
    date: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
  },
  {
    id: 'seed-02',
    nickname: 'Satoru Gojo',
    anime: 'jujutsu-kaisen',
    mode: 'time-attack',
    totalScore: 500,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 7.2,
    date: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
  },
  {
    id: 'seed-03',
    nickname: 'Lionel Messi',
    anime: 'football',
    mode: 'classic',
    totalScore: 500,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 8.4,
    date: new Date(Date.now() - 1000 * 60 * 180).toISOString(),
  },
  {
    id: 'seed-04',
    nickname: 'Tony Stark',
    anime: 'marvel',
    mode: 'classic',
    totalScore: 480,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 10.5,
    date: new Date(Date.now() - 1000 * 60 * 240).toISOString(),
  },
  {
    id: 'seed-05',
    nickname: 'Cinephile Nolan',
    anime: 'movies',
    mode: 'classic',
    totalScore: 480,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 12.1,
    date: new Date(Date.now() - 1000 * 60 * 360).toISOString(),
  },
  {
    id: 'seed-06',
    nickname: 'Gon Freecss',
    anime: 'hunter-x-hunter',
    mode: 'classic',
    totalScore: 460,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 14.3,
    date: new Date(Date.now() - 1000 * 60 * 480).toISOString(),
  },
  {
    id: 'seed-07',
    nickname: 'Kakashi Hatake',
    anime: 'naruto',
    mode: 'classic',
    totalScore: 460,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 15.0,
    date: new Date(Date.now() - 1000 * 60 * 720).toISOString(),
  },
  {
    id: 'seed-08',
    nickname: 'Cristiano Ronaldo',
    anime: 'football',
    mode: 'time-attack',
    totalScore: 440,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 13.8,
    date: new Date(Date.now() - 1000 * 60 * 900).toISOString(),
  },
  {
    id: 'seed-09',
    nickname: 'Roronoa Zoro',
    anime: 'one-piece',
    mode: 'classic',
    totalScore: 440,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 17.6,
    date: new Date(Date.now() - 1000 * 60 * 1100).toISOString(),
  },
  {
    id: 'seed-10',
    nickname: 'Kurapika Kurta',
    anime: 'hunter-x-hunter',
    mode: 'classic',
    totalScore: 420,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 19.2,
    date: new Date(Date.now() - 1000 * 60 * 1440).toISOString(),
  },
  {
    id: 'seed-11',
    nickname: 'Peter Parker',
    anime: 'marvel',
    mode: 'classic',
    totalScore: 420,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 20.4,
    date: new Date(Date.now() - 1000 * 60 * 1800).toISOString(),
  },
  {
    id: 'seed-12',
    nickname: 'Tarantino Fan',
    anime: 'movies',
    mode: 'time-attack',
    totalScore: 400,
    correctGuesses: 5,
    totalRounds: 5,
    bestTime: 22.0,
    date: new Date(Date.now() - 1000 * 60 * 2200).toISOString(),
  },
];

// ── Leaderboard ─────────────────────────────────────────────
export function getLeaderboard(): LeaderboardEntry[] {
  try {
    const raw = localStorage.getItem(LEADERBOARD_KEY);
    if (!raw) {
      localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(DEFAULT_LEADERBOARD_ENTRIES));
      return DEFAULT_LEADERBOARD_ENTRIES;
    }
    const parsed: LeaderboardEntry[] = JSON.parse(raw);
    if (!Array.isArray(parsed) || parsed.length === 0) {
      localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(DEFAULT_LEADERBOARD_ENTRIES));
      return DEFAULT_LEADERBOARD_ENTRIES;
    }
    return parsed;
  } catch {
    return DEFAULT_LEADERBOARD_ENTRIES;
  }
}

export function addLeaderboardEntry(entry: LeaderboardEntry): void {
  const board = getLeaderboard();
  board.push(entry);
  // Ensure all players are preserved (up to 1,000 entries)
  const sorted = board.sort((a, b) => b.totalScore - a.totalScore).slice(0, 1000);
  localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(sorted));
}

export function clearLeaderboard(): void {
  localStorage.setItem(LEADERBOARD_KEY, JSON.stringify([]));
}

export function resetLeaderboard(): void {
  localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(DEFAULT_LEADERBOARD_ENTRIES));
}

// ── User Preferences ─────────────────────────────────────────
export interface UserPrefs {
  nickname: string;
  lastAnime: string;
  lastMode: string;
  lastDifficulty: string[];
}

export function getPrefs(): UserPrefs {
  try {
    const raw = localStorage.getItem(PREFS_KEY);
    return raw
      ? JSON.parse(raw)
      : { nickname: '', lastAnime: 'hunter-x-hunter', lastMode: 'classic', lastDifficulty: ['easy', 'medium'] };
  } catch {
    return { nickname: '', lastAnime: 'hunter-x-hunter', lastMode: 'classic', lastDifficulty: ['easy', 'medium'] };
  }
}

export function savePrefs(prefs: Partial<UserPrefs>): void {
  const current = getPrefs();
  localStorage.setItem(PREFS_KEY, JSON.stringify({ ...current, ...prefs }));
}

// ── Score calculation ─────────────────────────────────────────
export function calculateScore(elapsedSeconds: number): number {
  if (elapsedSeconds < 30) return 100;
  if (elapsedSeconds < 60) return 80;
  if (elapsedSeconds < 90) return 60;
  if (elapsedSeconds < 120) return 40;
  return 0;
}

export function sessionToLeaderboardEntry(
  session: GameSession,
  nickname: string
): LeaderboardEntry {
  const correctRounds = session.rounds.filter((r: RoundResult) => r.isCorrect);
  const bestTime =
    correctRounds.length > 0
      ? Math.min(...correctRounds.map((r: RoundResult) => r.timeElapsed))
      : 0;

  return {
    id: `${Date.now()}-${Math.random().toString(36).slice(2)}`,
    nickname: nickname.trim() || 'Examinee',
    anime: session.anime,
    mode: session.mode,
    totalScore: session.totalScore,
    correctGuesses: correctRounds.length,
    totalRounds: session.rounds.length,
    bestTime,
    date: new Date().toISOString(),
  };
}

export function recordMovieScore(
  nickname: string,
  mode: GameMode,
  totalScore: number,
  correctGuesses: number,
  totalRounds: number,
  bestTime: number
): LeaderboardEntry {
  const entry: LeaderboardEntry = {
    id: `mov-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    nickname: nickname.trim() || 'Cinephile',
    anime: 'movies',
    mode,
    totalScore,
    correctGuesses,
    totalRounds,
    bestTime,
    date: new Date().toISOString(),
  };
  addLeaderboardEntry(entry);
  return entry;
}
