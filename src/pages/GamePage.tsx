import { useState, useCallback, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import type { AnimeUniverse, GameConfig, GameMode, Difficulty, GameSession, RoundResult, Character } from '../types';
import { ANIME_META, BLUR_STAGES, HINT_TIMES, ROUND_DURATION } from '../types';
import { filterCharacters, selectRandomCharacter, shuffleArray } from '../services/characterService';
import { validateAnswer } from '../services/answerValidator';
import { calculateScore, getPrefs, savePrefs, addLeaderboardEntry, sessionToLeaderboardEntry } from '../services/storageService';
import { useGameTimer } from '../hooks/useGameTimer';
import ConfigScreen from '../components/ConfigScreen/ConfigScreen';
import GameScreen from '../components/GameScreen/GameScreen';
import ResultScreen from '../components/ResultScreen/ResultScreen';
import SessionSummary from '../components/SessionSummary/SessionSummary';

type PageState = 'config' | 'playing' | 'result' | 'summary';

export default function GamePage() {
  const { anime } = useParams<{ anime: string }>();
  const navigate = useNavigate();
  const animeUniverse = anime as AnimeUniverse;
  const meta = ANIME_META[animeUniverse];

  if (!meta) {
    navigate('/');
    return null;
  }

  return <GamePageInner anime={animeUniverse} />;
}

function GamePageInner({ anime }: { anime: AnimeUniverse }) {
  const navigate = useNavigate();
  const meta = ANIME_META[anime];
  const prefs = getPrefs();

  const [pageState, setPageState] = useState<PageState>('config');

  const defaultDiff: Difficulty[] = ['easy', 'medium', 'hard', 'expert'];
  const savedDiff = prefs.lastDifficulty as Difficulty[] | undefined;
  const initialDifficulty = (savedDiff && savedDiff.length > 2) ? savedDiff : defaultDiff;

  const [config, setConfig] = useState<GameConfig>({
    anime,
    mode: (prefs.lastMode as GameMode) || 'classic',
    difficulty: initialDifficulty,
    rounds: 5,
    includeAnimeOnly: true,
    includeManga: false,
    spoilerLevel: 1,
  });

  const [session, setSession] = useState<GameSession | null>(null);
  const [currentRound, setCurrentRound] = useState(0);
  const [currentCharacter, setCurrentCharacter] = useState<Character | null>(null);
  const [guess, setGuess] = useState('');
  const [roundStatus, setRoundStatus] = useState<'playing' | 'correct' | 'timeout'>('playing');
  const [hintsRevealed, setHintsRevealed] = useState(0);
  const [lastResult, setLastResult] = useState<RoundResult | null>(null);
  const [incorrectFlash, setIncorrectFlash] = useState(false);

  // Use refs for mutable values needed inside callbacks
  const currentCharRef = useRef<Character | null>(null);
  const hintsRevealedRef = useRef(0);
  const guessRef = useRef('');
  const roundStatusRef = useRef<'playing' | 'correct' | 'timeout'>('playing');
  const sessionRef = useRef<GameSession | null>(null);
  const poolRef = useRef<Character[]>([]);
  const usedIdsRef = useRef<string[]>([]);
  const recentPlayedIdsRef = useRef<string[]>([]);
  const currentRoundRef = useRef(0);
  const configRef = useRef(config);

  const startTimerRef = useRef<() => void>(() => {});
  const stopTimerRef = useRef<() => void>(() => {});
  const resetTimerRef = useRef<() => void>(() => {});

  const handleExpire = useCallback(() => {
    if (roundStatusRef.current === 'playing') {
      doEndRound(false, ROUND_DURATION);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const { elapsedTime, start: startTimer, stop: stopTimer, reset: resetTimer } = useGameTimer(
    (elapsed) => {
      let revealed = 0;
      for (const t of HINT_TIMES) { if (elapsed >= t) revealed++; }
      hintsRevealedRef.current = revealed;
      setHintsRevealed(revealed);
    },
    handleExpire
  );

  startTimerRef.current = startTimer;
  stopTimerRef.current = stopTimer;
  resetTimerRef.current = resetTimer;

  const getBlur = (elapsed: number): number => {
    const stages = [...BLUR_STAGES].reverse();
    for (const s of stages) { if (elapsed >= s.time) return s.blur; }
    return 28;
  };

  // ── doEndRound – called from submit or timer expiry ──────
  function doEndRound(isCorrect: boolean, elapsed: number) {
    stopTimerRef.current();
    roundStatusRef.current = isCorrect ? 'correct' : 'timeout';
    setRoundStatus(isCorrect ? 'correct' : 'timeout');

    const points = isCorrect ? calculateScore(elapsed) : 0;
    const result: RoundResult = {
      character: currentCharRef.current!,
      isCorrect,
      timeElapsed: elapsed,
      hintsRevealed: hintsRevealedRef.current,
      pointsEarned: points,
      guess: isCorrect ? guessRef.current : undefined,
    };
    setLastResult(result);

    const prevSession = sessionRef.current!;
    const updatedSession: GameSession = {
      ...prevSession,
      rounds: [...prevSession.rounds, result],
      totalScore: prevSession.totalScore + points,
    };
    sessionRef.current = updatedSession;
    setSession(updatedSession);

    setTimeout(() => setPageState('result'), 2000);
  }

  // ── beginRound ───────────────────────────────────────────
  function beginRound(
    characters: Character[],
    used: string[],
    sess: GameSession,
    cfg: GameConfig
  ) {
    const available = characters.filter(c => !used.includes(c.id));
    // Prioritize candidates not recently played to guarantee high variety across sessions
    const unplayedRecently = available.filter(c => !recentPlayedIdsRef.current.includes(c.id));
    const poolToPickFrom = unplayedRecently.length > 0 ? unplayedRecently : available;
    const char = selectRandomCharacter(poolToPickFrom);

    if (!char) {
      if (sess) {
        const latestPrefs = getPrefs();
        const entry = sessionToLeaderboardEntry(sess, latestPrefs.nickname || 'Hunter');
        addLeaderboardEntry(entry);
      }
      setSession(sess);
      setPageState('summary');
      return;
    }

    const newUsed = [...used, char.id];
    usedIdsRef.current = newUsed;
    recentPlayedIdsRef.current = [...recentPlayedIdsRef.current.filter(id => id !== char.id), char.id];
    // Keep sliding window of played IDs
    const maxRecent = Math.max(10, characters.length - 5);
    if (recentPlayedIdsRef.current.length > maxRecent) {
      recentPlayedIdsRef.current.splice(0, recentPlayedIdsRef.current.length - maxRecent);
    }

    currentCharRef.current = char;
    setCurrentCharacter(char);
    guessRef.current = '';
    setGuess('');
    hintsRevealedRef.current = 0;
    setHintsRevealed(0);
    roundStatusRef.current = 'playing';
    setRoundStatus('playing');
    setIncorrectFlash(false);

    sessionRef.current = sess;
    configRef.current = cfg;

    resetTimerRef.current();
    setPageState('playing');
    setTimeout(() => startTimerRef.current(), 150);
  }

  // ── startGame ────────────────────────────────────────────
  const startGame = (newCfg: GameConfig) => {
    savePrefs({ lastMode: newCfg.mode, lastDifficulty: newCfg.difficulty, lastAnime: newCfg.anime });
    setConfig(newCfg);
    configRef.current = newCfg;

    const characters = filterCharacters(newCfg);
    if (characters.length === 0) {
      alert('No characters found with these filters. Please adjust your settings.');
      return;
    }

    const shuffledPool = shuffleArray(characters);

    const newSession: GameSession = {
      id: `${Date.now()}`,
      anime: newCfg.anime,
      mode: newCfg.mode,
      difficulty: newCfg.difficulty,
      rounds: [],
      totalScore: 0,
      startedAt: Date.now(),
    };

    poolRef.current = shuffledPool;
    usedIdsRef.current = [];
    sessionRef.current = newSession;
    setSession(newSession);
    currentRoundRef.current = 0;
    setCurrentRound(0);

    beginRound(shuffledPool, [], newSession, newCfg);
  };

  // ── handleGuess ──────────────────────────────────────────
  const handleGuess = useCallback(() => {
    if (roundStatusRef.current !== 'playing' || !currentCharRef.current || !guessRef.current.trim()) return;
    const isCorrect = validateAnswer(guessRef.current, currentCharRef.current);
    if (isCorrect) {
      doEndRound(true, elapsedTime);
    } else {
      setIncorrectFlash(true);
      setTimeout(() => setIncorrectFlash(false), 600);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [elapsedTime]);

  // ── handleNext ───────────────────────────────────────────
  const handleNext = useCallback(() => {
    const nextRound = currentRoundRef.current + 1;
    currentRoundRef.current = nextRound;
    setCurrentRound(nextRound);

    const cfg = configRef.current;
    const maxRounds = cfg.mode === 'endless' ? Infinity : cfg.rounds;
    const sess = sessionRef.current!;

    if (nextRound >= maxRounds) {
      const latestPrefs = getPrefs();
      const entry = sessionToLeaderboardEntry(sess, latestPrefs.nickname || 'Hunter');
      addLeaderboardEntry(entry);
      setPageState('summary');
      return;
    }

    beginRound(poolRef.current, usedIdsRef.current, sess, cfg);
  }, []);

  const handleEndSession = useCallback(() => {
    if (sessionRef.current) {
      const latestPrefs = getPrefs();
      const entry = sessionToLeaderboardEntry(sessionRef.current, latestPrefs.nickname || 'Hunter');
      addLeaderboardEntry(entry);
    }
    setPageState('summary');
  }, []);

  const handleReplay = () => startGame(configRef.current);

  const handleGuessChange = (v: string) => {
    guessRef.current = v;
    setGuess(v);
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-dark)', position: 'relative' }}>
      <div style={{
        position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 0,
        background: `radial-gradient(ellipse at top, ${meta.glow} 0%, transparent 60%)`,
      }} />

      <AnimatePresence mode="wait">
        {pageState === 'config' && (
          <motion.div key="config"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <ConfigScreen
              anime={anime}
              initialConfig={config}
              onStart={startGame}
              onBack={() => navigate('/')}
            />
          </motion.div>
        )}

        {pageState === 'playing' && currentCharacter && (
          <motion.div key="playing"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <GameScreen
              anime={anime}
              character={currentCharacter}
              elapsedTime={elapsedTime}
              hintsRevealed={hintsRevealed}
              blur={roundStatus !== 'playing' ? 0 : getBlur(elapsedTime)}
              roundStatus={roundStatus}
              guess={guess}
              onGuessChange={handleGuessChange}
              onSubmit={handleGuess}
              incorrectFlash={incorrectFlash}
              roundNumber={currentRound + 1}
              totalRounds={config.mode === 'endless' ? null : config.rounds}
              mode={config.mode}
            />
          </motion.div>
        )}

        {pageState === 'result' && lastResult && (
          <motion.div key="result"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <ResultScreen
              result={lastResult}
              anime={anime}
              totalScore={session?.totalScore ?? 0}
              roundNumber={currentRound + 1}
              totalRounds={config.mode === 'endless' ? null : config.rounds}
              mode={config.mode}
              onNext={handleNext}
              onReplay={handleReplay}
              onHome={() => navigate('/')}
              onEndSession={handleEndSession}
            />
          </motion.div>
        )}

        {pageState === 'summary' && session && (
          <motion.div key="summary"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <SessionSummary
              session={session}
              onReplay={handleReplay}
              onHome={() => navigate('/')}
              onLeaderboard={() => navigate('/leaderboard')}
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
