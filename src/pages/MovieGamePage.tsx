import { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ArrowLeft,
  Film,
  Clapperboard,
  Clock,
  Send,
  SkipForward,
  Trophy,
  RotateCcw,
  User,
  Check,
  AlertCircle,
  Award,
  Sparkles,
  EyeOff,
} from 'lucide-react';
import { MOVIES, type Movie } from '../data/movies/movies';
import { validateMovieGuess } from '../services/answerValidator';
import { recordMovieScore, getPrefs, savePrefs } from '../services/storageService';
import type { GameMode, Difficulty } from '../types';
import { SpiderWebBackground } from '../components/common/SpiderWebBackground';
import styles from './MovieGamePage.module.css';

type PageState = 'config' | 'playing' | 'result' | 'summary';

interface MovieRoundResult {
  movie: Movie;
  isCorrect: boolean;
  timeElapsed: number;
  hintsRevealed: number;
  pointsEarned: number;
  guess?: string;
}

const ERAS = [
  'All Eras',
  'Classic Era',
  '90s Renaissance',
  '2000s Modern Classics',
  '2010s Blockbusters',
  '2020s Visionary',
];

const DIFFICULTIES: { id: Difficulty; label: string; color: string }[] = [
  { id: 'easy', label: 'EASY', color: '#4ADE80' },
  { id: 'medium', label: 'MEDIUM', color: '#FACC15' },
  { id: 'hard', label: 'HARD', color: '#F97316' },
  { id: 'expert', label: 'EXPERT', color: '#EF4444' },
];

export default function MovieGamePage() {
  const navigate = useNavigate();
  const prefs = getPrefs();

  const [pageState, setPageState] = useState<PageState>('config');
  const [nickname, setNickname] = useState(prefs.nickname && prefs.nickname !== 'Hunter' ? prefs.nickname : '');
  const [nameError, setNameError] = useState<string | null>(null);
  const [mode, setMode] = useState<GameMode>('classic');
  const [selectedDifficulty, setSelectedDifficulty] = useState<Difficulty[]>(['easy', 'medium', 'hard']);
  const [selectedEra, setSelectedEra] = useState<string>('All Eras');
  const [roundsCount, setRoundsCount] = useState<number>(5);

  // Gameplay state
  const [pool, setPool] = useState<Movie[]>([]);
  const [usedIds, setUsedIds] = useState<string[]>([]);
  const [currentRound, setCurrentRound] = useState<number>(0);
  const [currentMovie, setCurrentMovie] = useState<Movie | null>(null);
  const [elapsedTime, setElapsedTime] = useState<number>(0);
  const [guess, setGuess] = useState<string>('');
  const [incorrectFlash, setIncorrectFlash] = useState<boolean>(false);
  const [results, setResults] = useState<MovieRoundResult[]>([]);
  const [lastRoundResult, setLastRoundResult] = useState<MovieRoundResult | null>(null);
  const [totalScore, setTotalScore] = useState<number>(0);

  const timerRef = useRef<number | null>(null);
  const roundActiveRef = useRef<boolean>(false);

  // Filter available pool
  const filterMovies = useCallback(() => {
    return MOVIES.filter(m => {
      const diffMatch = selectedDifficulty.includes(m.difficulty);
      const eraMatch = selectedEra === 'All Eras' || m.era === selectedEra;
      return diffMatch && eraMatch;
    });
  }, [selectedDifficulty, selectedEra]);

  const activeMatchingCount = filterMovies().length;

  // Toggle difficulty
  const toggleDifficulty = (d: Difficulty) => {
    setSelectedDifficulty(prev => {
      if (prev.includes(d) && prev.length === 1) return prev;
      return prev.includes(d) ? prev.filter(x => x !== d) : [...prev, d];
    });
  };

  // Timer logic
  const stopTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    roundActiveRef.current = false;
  };

  const startTimer = () => {
    stopTimer();
    roundActiveRef.current = true;
    setElapsedTime(0);
    const start = Date.now();
    timerRef.current = window.setInterval(() => {
      const elapsed = Math.floor((Date.now() - start) / 1000);
      setElapsedTime(elapsed);
      if (elapsed >= 120) {
        stopTimer();
        handleRoundTimeout();
      }
    }, 250);
  };

  useEffect(() => {
    return () => stopTimer();
  }, []);

  // Calculate points
  const calculatePoints = (time: number): number => {
    if (time < 30) return 100;
    if (time < 60) return 80;
    if (time < 90) return 60;
    if (time < 120) return 40;
    return 0;
  };

  // Begin next round
  const beginRound = (moviePool: Movie[], used: string[]) => {
    const available = moviePool.filter(m => !used.includes(m.id));
    if (available.length === 0) {
      endGameSession();
      return;
    }

    const nextMovie = available[Math.floor(Math.random() * available.length)];
    setCurrentMovie(nextMovie);
    setUsedIds([...used, nextMovie.id]);
    setGuess('');
    setIncorrectFlash(false);
    setPageState('playing');
    startTimer();
  };

  // Start game session
  const handleStartGame = () => {
    const clean = nickname.trim();
    if (!clean) {
      setNameError('Please enter an examinee nickname to track your ranking.');
      return;
    }
    setNameError(null);
    savePrefs({ nickname: clean });

    const filtered = filterMovies();
    if (filtered.length === 0) {
      alert('No movies match these filters. Please broaden your selection.');
      return;
    }

    setPool(filtered);
    setUsedIds([]);
    setResults([]);
    setTotalScore(0);
    setCurrentRound(0);

    beginRound(filtered, []);
  };

  // Handle round completion
  const handleRoundEnd = (isCorrect: boolean, time: number) => {
    stopTimer();
    if (!currentMovie) return;

    const points = isCorrect ? calculatePoints(time) : 0;
    const revealedHintsCount = currentMovie.hints.filter(h => time >= h.timeRevealed).length;

    const roundRes: MovieRoundResult = {
      movie: currentMovie,
      isCorrect,
      timeElapsed: time,
      hintsRevealed: revealedHintsCount,
      pointsEarned: points,
      guess,
    };

    const updatedResults = [...results, roundRes];
    const updatedScore = totalScore + points;

    setResults(updatedResults);
    setTotalScore(updatedScore);
    setLastRoundResult(roundRes);
    setPageState('result');
  };

  const handleRoundTimeout = () => {
    handleRoundEnd(false, 120);
  };

  // Guess submission
  const handleGuessSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!roundActiveRef.current || !currentMovie || !guess.trim()) return;

    const isMatch = validateMovieGuess(guess, currentMovie);
    if (isMatch) {
      handleRoundEnd(true, elapsedTime);
    } else {
      setIncorrectFlash(true);
      setTimeout(() => setIncorrectFlash(false), 500);
    }
  };

  // Skip movie
  const handleSkip = () => {
    if (!roundActiveRef.current) return;
    handleRoundEnd(false, elapsedTime);
  };

  // Next round
  const handleNextRound = () => {
    const nextIdx = currentRound + 1;
    setCurrentRound(nextIdx);

    const maxRounds = mode === 'endless' ? Infinity : roundsCount;
    if (nextIdx >= maxRounds || usedIds.length >= pool.length) {
      endGameSession();
      return;
    }

    beginRound(pool, usedIds);
  };

  // End game & save to leaderboard
  const endGameSession = () => {
    stopTimer();
    const correctCount = results.filter(r => r.isCorrect).length;
    const bestTime = correctCount > 0
      ? Math.min(...results.filter(r => r.isCorrect).map(r => r.timeElapsed))
      : 0;

    // Save to leaderboard immediately
    recordMovieScore(
      nickname || 'Cinephile',
      mode,
      totalScore,
      correctCount,
      results.length,
      bestTime
    );

    setPageState('summary');
  };

  return (
    <div className={styles.page}>
      <SpiderWebBackground universe="movies" />

      {/* Top Header */}
      <header className={styles.header}>
        <button className={styles.backBtn} onClick={() => navigate('/')}>
          <ArrowLeft size={16} /> MAIN HUB
        </button>
        <div className={styles.headerCenter}>
          <div className={styles.headerMarqueeBadge}>
            <Clapperboard size={12} />
            <span>CINEMA DEDUCTION CHAMBER</span>
          </div>
          <h1 className={styles.headerTitle}>GUESS THE MOVIE</h1>
        </div>
        <div className={styles.headerRight}>
          <div className={styles.scorePill}>
            <Trophy size={14} />
            <span>{totalScore} PTS</span>
          </div>
        </div>
      </header>

      <main className={styles.container}>
        {/* ============================================================ */}
        {/* 1. CONFIG STATE                                              */}
        {/* ============================================================ */}
        {pageState === 'config' && (
          <motion.div
            className={styles.configCard}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <div className={styles.configHero}>
              <Film size={44} className={styles.filmReelIcon} />
              <h2 className={styles.configHeroTitle}>CINEMA INTELLECT TRIAL</h2>
              <p className={styles.configHeroSub}>
                Test your mastery of legendary filmmaking. Deduce the exact movie title strictly through progressive narrative hints, director styles, key characters, and famous quotes.
              </p>
              <div className={styles.noPhotosNotice}>
                <EyeOff size={14} />
                <span>NO PHOTOS ALLOWED • PURE TEXT DEDUCTION</span>
              </div>
            </div>

            {/* Examinee Nickname */}
            <div className={styles.nameSection}>
              <label className={styles.sectionLabel}>
                <span>EXAMINEE CANDIDATE NAME (REQUIRED)</span>
                <Award size={14} />
              </label>
              <div className={styles.inputGroup}>
                <User size={18} className={styles.inputIcon} />
                <input
                  type="text"
                  className={styles.textInput}
                  placeholder="Enter your Cinephile alias..."
                  value={nickname}
                  onChange={e => {
                    setNickname(e.target.value);
                    if (e.target.value.trim()) setNameError(null);
                  }}
                  onKeyDown={e => e.key === 'Enter' && handleStartGame()}
                  maxLength={24}
                />
              </div>
              {nameError && (
                <div className={styles.errorText}>
                  <AlertCircle size={14} /> {nameError}
                </div>
              )}
            </div>

            {/* Game Mode */}
            <div>
              <div className={styles.sectionLabel}>
                <span>GAME MODE</span>
                <span style={{ color: '#94A3B8', fontSize: '11px' }}>{mode.toUpperCase()}</span>
              </div>
              <div className={styles.chipGrid}>
                {[
                  { id: 'classic' as GameMode, label: 'CLASSIC (TIMED)' },
                  { id: 'time-attack' as GameMode, label: 'TIME ATTACK' },
                  { id: 'endless' as GameMode, label: 'ENDLESS REEL' },
                ].map(m => (
                  <button
                    key={m.id}
                    type="button"
                    className={`${styles.chip} ${mode === m.id ? styles.chipActive : ''}`}
                    onClick={() => setMode(m.id)}
                  >
                    {mode === m.id && <Check size={12} />}
                    {m.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Difficulty Filter */}
            <div>
              <div className={styles.sectionLabel}>
                <span>DIFFICULTY TIERS</span>
                <span style={{ color: '#94A3B8', fontSize: '11px' }}>MULTI-SELECT</span>
              </div>
              <div className={styles.chipGrid}>
                {DIFFICULTIES.map(d => {
                  const active = selectedDifficulty.includes(d.id);
                  return (
                    <button
                      key={d.id}
                      type="button"
                      className={`${styles.chip} ${active ? styles.chipActive : ''}`}
                      onClick={() => toggleDifficulty(d.id)}
                    >
                      {active && <Check size={12} />}
                      <span style={{ color: d.color, fontWeight: 'bold' }}>•</span>
                      {d.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Era Filter */}
            <div>
              <div className={styles.sectionLabel}>
                <span>FILM ERA & SAGA FILTER</span>
                <span style={{ color: '#94A3B8', fontSize: '11px' }}>{activeMatchingCount} FILMS READY</span>
              </div>
              <div className={styles.chipGrid}>
                {ERAS.map(era => {
                  const active = selectedEra === era;
                  return (
                    <button
                      key={era}
                      type="button"
                      className={`${styles.chip} ${active ? styles.chipActive : ''}`}
                      onClick={() => setSelectedEra(era)}
                    >
                      {active && <Check size={12} />}
                      {era}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Rounds Selector */}
            <div>
              <div className={styles.sectionLabel}>
                <span>NUMBER OF ROUNDS</span>
                <span style={{ color: '#94A3B8', fontSize: '11px' }}>{roundsCount} FILMS</span>
              </div>
              <div className={styles.chipGrid}>
                {[3, 5, 10, 15, 20].map(n => (
                  <button
                    key={n}
                    type="button"
                    className={`${styles.chip} ${roundsCount === n ? styles.chipActive : ''}`}
                    onClick={() => setRoundsCount(n)}
                  >
                    {n} ROUNDS
                  </button>
                ))}
              </div>
            </div>

            {/* Launch Button */}
            <motion.button
              className={styles.startMovieBtn}
              onClick={handleStartGame}
              disabled={activeMatchingCount === 0}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Clapperboard size={18} />
              <span>ROLL CAMERA & START ({activeMatchingCount} AVAILABLE)</span>
            </motion.button>
          </motion.div>
        )}

        {/* ============================================================ */}
        {/* 2. PLAYING STATE                                             */}
        {/* ============================================================ */}
        {pageState === 'playing' && currentMovie && (
          <motion.div
            className={styles.playingWrap}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            {/* Status Bar */}
            <div className={styles.statusBar}>
              <div className={styles.roundInfo}>
                <span className={styles.roundNumber}>
                  ROUND {currentRound + 1} OF {mode === 'endless' ? '∞' : roundsCount} • {currentMovie.era.toUpperCase()}
                </span>
                <div className={styles.genreTags}>
                  {currentMovie.genres.map(g => (
                    <span key={g} className={styles.genreTag}>{g}</span>
                  ))}
                  {currentMovie.oscarsWon && currentMovie.oscarsWon > 0 && (
                    <span className={styles.genreTag} style={{ color: '#FACC15', borderColor: '#FACC15' }}>
                      ★ {currentMovie.oscarsWon} OSCARS
                    </span>
                  )}
                </div>
              </div>

              <div className={styles.timerBox}>
                <Clock size={18} color="#F43F5E" />
                <span className={`${styles.timerVal} ${elapsedTime >= 90 ? styles.timerUrgent : ''}`}>
                  {120 - elapsedTime}s
                </span>
              </div>
            </div>

            {/* Progressive Hint Board (NO PHOTOS) */}
            <div className={styles.clueBoard}>
              {currentMovie.hints.map((hint, idx) => {
                const isRevealed = elapsedTime >= hint.timeRevealed;
                return (
                  <div
                    key={idx}
                    className={`${styles.clueCard} ${isRevealed ? styles.clueCardRevealed : styles.clueCardLocked}`}
                  >
                    <div className={`${styles.clueBadge} ${isRevealed ? styles.clueBadgeActive : ''}`}>
                      {idx + 1}
                    </div>
                    <div className={styles.clueContent}>
                      <div className={styles.clueLabel}>
                        CLUE #{idx + 1} • {hint.label}
                        {!isRevealed && ` (Unlocks in ${hint.timeRevealed - elapsedTime}s)`}
                      </div>
                      {isRevealed ? (
                        <p className={styles.clueText}>{hint.text}</p>
                      ) : (
                        <p className={styles.clueLockedText}>
                          🔒 Mystery clue classified. Watch the timer as director intelligence declassifies...
                        </p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Guess Input Bar */}
            <form onSubmit={handleGuessSubmit} className={styles.guessBar}>
              <input
                type="text"
                className={`${styles.guessInput} ${incorrectFlash ? styles.guessInputFlash : ''}`}
                placeholder="Type the movie title and press Enter (e.g. Inception, The Dark Knight)..."
                value={guess}
                onChange={e => setGuess(e.target.value)}
                autoFocus
              />
              <button type="submit" className={styles.submitBtn}>
                <Send size={16} /> GUESS
              </button>
              <button type="button" className={styles.skipBtn} onClick={handleSkip}>
                <SkipForward size={14} /> SKIP
              </button>
            </form>
          </motion.div>
        )}

        {/* ============================================================ */}
        {/* 3. ROUND RESULT STATE                                        */}
        {/* ============================================================ */}
        {pageState === 'result' && lastRoundResult && (
          <motion.div
            className={styles.resultCard}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <div style={{ color: lastRoundResult.isCorrect ? '#4ADE80' : '#EF4444' }}>
              {lastRoundResult.isCorrect ? <Sparkles size={48} /> : <AlertCircle size={48} />}
            </div>

            <h2 className={styles.resultTitle}>
              {lastRoundResult.isCorrect ? 'BRILLIANT DEDUCTION!' : 'CUT! FILM REVEALED'}
            </h2>

            <div style={{ fontSize: '26px', fontWeight: '900', color: '#FFF' }}>
              {lastRoundResult.movie.title} ({lastRoundResult.movie.year})
            </div>

            <p className={styles.resultTagline}>
              "{lastRoundResult.movie.tagline}"
            </p>

            <div className={styles.resultMetaRow}>
              <span>Director: <strong>{lastRoundResult.movie.director}</strong></span>
              <span>•</span>
              <span>Cast: <strong>{lastRoundResult.movie.cast.slice(0, 3).join(', ')}</strong></span>
            </div>

            <div className={styles.pointsEarned}>
              +{lastRoundResult.pointsEarned} POINTS ({lastRoundResult.timeElapsed}s)
            </div>

            <button className={styles.startMovieBtn} onClick={handleNextRound}>
              NEXT FILM →
            </button>
          </motion.div>
        )}

        {/* ============================================================ */}
        {/* 4. SUMMARY STATE                                             */}
        {/* ============================================================ */}
        {pageState === 'summary' && (
          <motion.div
            className={styles.summaryCard}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <div className={styles.summaryHeader}>
              <Trophy size={48} color="#F43F5E" />
              <div className={styles.summaryScore}>{totalScore}</div>
              <div className={styles.summaryScoreLabel}>TOTAL CINEPHILE POINTS</div>
              <p style={{ color: '#94A3B8', marginTop: '8px' }}>
                Examinee: <strong>{nickname || 'Cinephile'}</strong> • Saved to Global Leaderboard
              </p>
            </div>

            <div className={styles.statsRow}>
              <div className={styles.statBox}>
                <div className={styles.statVal}>
                  {results.filter(r => r.isCorrect).length} / {results.length}
                </div>
                <div className={styles.statLabel}>CORRECT FILMS</div>
              </div>
              <div className={styles.statBox}>
                <div className={styles.statVal}>
                  {results.length > 0
                    ? `${Math.round((results.filter(r => r.isCorrect).length / results.length) * 100)}%`
                    : '0%'}
                </div>
                <div className={styles.statLabel}>ACCURACY</div>
              </div>
              <div className={styles.statBox}>
                <div className={styles.statVal}>
                  {results.filter(r => r.isCorrect).length > 0
                    ? `${Math.min(...results.filter(r => r.isCorrect).map(r => r.timeElapsed))}s`
                    : '--'}
                </div>
                <div className={styles.statLabel}>FASTEST GUESS</div>
              </div>
            </div>

            <div className={styles.actionRow}>
              <button className={styles.startMovieBtn} onClick={() => setPageState('config')}>
                <RotateCcw size={16} /> PLAY AGAIN
              </button>
              <button
                className={styles.backBtn}
                style={{ padding: '14px 24px', fontSize: '13px' }}
                onClick={() => navigate('/leaderboard')}
              >
                <Trophy size={16} /> VIEW LEADERBOARD
              </button>
            </div>
          </motion.div>
        )}
      </main>
    </div>
  );
}
