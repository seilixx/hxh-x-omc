import { useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Eye, ShieldAlert, User } from 'lucide-react';
import type { AnimeUniverse, GameMode, Character } from '../../types';
import { ROUND_DURATION, ANIME_META } from '../../types';
import CharacterPortrait from '../CharacterPortrait/CharacterPortrait';
import { SpiderWebBackground } from '../common/SpiderWebBackground';
import { getPrefs } from '../../services/storageService';
import styles from './GameScreen.module.css';

interface Props {
  anime: AnimeUniverse;
  character: Character;
  elapsedTime: number;
  hintsRevealed: number;
  blur: number;
  roundStatus: 'playing' | 'correct' | 'timeout';
  guess: string;
  onGuessChange: (v: string) => void;
  onSubmit: () => void;
  incorrectFlash: boolean;
  roundNumber: number;
  totalRounds: number | null;
  mode: GameMode;
}

export default function GameScreen({
  anime,
  character,
  elapsedTime,
  hintsRevealed,
  blur,
  roundStatus,
  guess,
  onGuessChange,
  onSubmit,
  incorrectFlash,
  roundNumber,
  totalRounds,
  mode,
}: Props) {
  const meta = ANIME_META[anime];
  const inputRef = useRef<HTMLInputElement>(null);
  const prefs = getPrefs();
  const candidateName = prefs.nickname && prefs.nickname !== 'Hunter' ? prefs.nickname : 'Examinee #404';

  const remaining = ROUND_DURATION - elapsedTime;
  const mins = Math.floor(remaining / 60);
  const secs = remaining % 60;
  const timerStr = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  const isRevealed = roundStatus !== 'playing';
  const isCritical = remaining <= 30 && roundStatus === 'playing';
  const timerPercent = (elapsedTime / ROUND_DURATION) * 100;

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div
      className={styles.page}
      style={{ '--accent': meta.accent, '--glow': meta.glow } as React.CSSProperties}
    >
      {/* Dynamic Anime Character Background */}
      <SpiderWebBackground universe={anime} />

      {/* ── Top Bar ── */}
      <header className={styles.topBar}>
        <div className={styles.topLeft}>
          <div className={styles.omcBrand}>
            <img
              src="/assets/logos/Open Minds Logo.svg"
              alt="OMC"
              className={styles.omcMiniLogo}
            />
            <span className={styles.collabDivider}>|</span>
            <span className={styles.collabText}>HUNTER × HUNTER</span>
          </div>
          <span className={styles.animeTag}>{meta.shortLabel.toUpperCase()}</span>
          <span className={styles.roundTag}>
            ROUND {roundNumber}{totalRounds ? ` / ${totalRounds}` : ''}
          </span>
        </div>

        {/* Central Timer */}
        <div className={`${styles.timer} ${isCritical ? styles.timerCritical : ''}`}>
          <span className={styles.timerVal}>{timerStr}</span>
          {roundStatus === 'correct' && <span className={styles.timerLabel}>TARGET IDENTIFIED!</span>}
          {roundStatus === 'timeout' && <span className={styles.timerLabel}>EXAM TIME EXPIRED</span>}
          {roundStatus === 'playing' && (
            <span className={styles.timerLabel}>
              {remaining > 30 ? 'TIME REMAINING' : 'CRITICAL TIME WARNING'}
            </span>
          )}
        </div>

        <div className={styles.topRight}>
          <div className={styles.candidateBadge}>
            <User size={13} className={styles.candidateIcon} />
            <span className={styles.candidateNameText}>{candidateName}</span>
          </div>
          <span className={styles.modeTag}>{mode.toUpperCase()}</span>
        </div>
      </header>

      {/* Progress Line */}
      <div className={styles.timerBar}>
        <motion.div
          className={styles.timerFill}
          style={{ scaleX: 1 - timerPercent / 100, transformOrigin: 'left' }}
          animate={{ scaleX: 1 - timerPercent / 100 }}
          transition={{ duration: 0.05, ease: 'linear' }}
        />
      </div>

      {/* ── Main Content ── */}
      <main className={styles.main}>
        {/* Character Portrait with Dynamic Gaussian Blur */}
        <div className={styles.portraitWrap}>
          <CharacterPortrait
            character={character}
            anime={anime}
            blur={blur}
            isRevealed={isRevealed}
            roundStatus={roundStatus}
          />
        </div>

        {/* ── Right Control & Hint Panel ── */}
        <div className={styles.rightPanel}>
          {/* Machine Header */}
          <div className={styles.questionBox}>
            <div className={styles.examinerBadge}>
              <ShieldAlert size={12} />
              <span>THE EXAMINER ASKS</span>
            </div>
            <h2 className={styles.questionTitle}>WHO AM I?</h2>
            <p className={styles.questionSub}>
              Identify the candidate before the 2-minute deadline expires.
            </p>
            <div className={styles.questionLine} />
          </div>

          {/* Answer Input Section — Positioned right below question for instant accessibility */}
          {roundStatus === 'playing' ? (
            <motion.div
              className={`${styles.answerBox} ${incorrectFlash ? styles.answerWrong : ''}`}
              animate={incorrectFlash ? { x: [-8, 8, -6, 6, 0] } : {}}
              transition={{ duration: 0.35 }}
            >
              {incorrectFlash && (
                <p className={styles.wrongMsg}>INCORRECT ANSWER — KEEP GUESSING</p>
              )}
              <div className={styles.inputRow}>
                <input
                  ref={inputRef}
                  className={styles.input}
                  type="text"
                  value={guess}
                  onChange={e => onGuessChange(e.target.value)}
                  onKeyDown={handleKey}
                  placeholder="Enter name (English, Français, Romaji)..."
                  autoFocus
                  autoComplete="off"
                  spellCheck={false}
                />
                <button
                  className={styles.submitBtn}
                  onClick={onSubmit}
                  disabled={!guess.trim()}
                >
                  <Send size={15} />
                  GUESS
                </button>
              </div>
              <p className={styles.inputHint}>
                Press [Enter] to submit · English, Français & Romaji accepted
              </p>
            </motion.div>
          ) : (
            /* Post-round locked banner during reveal animation */
            <div className={styles.lockedBox}>
              <p className={styles.lockedText}>
                {roundStatus === 'correct'
                  ? '✓ CANDIDATE CONFIRMED — Transitioning to Exam Record...'
                  : '⏱ TIME EXPIRED — Candidate Identity Revealed...'}
              </p>
            </div>
          )}

          {/* Progressive Hints (Revealed at 0:30, 1:00, 1:30) */}
          <div className={styles.hintsBox}>
            <p className={styles.hintsLabel}>
              <Eye size={13} />
              PROGRESSIVE DOSSIER HINTS {hintsRevealed > 0 ? `(${hintsRevealed}/3)` : ''}
            </p>

            {character.hints.map((hint, i) => {
              const isVisible = (isRevealed && i < 3) || i < hintsRevealed;
              return (
                <AnimatePresence key={i}>
                  {isVisible ? (
                    <motion.div
                      className={styles.hint}
                      initial={{ opacity: 0, x: -14 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.4, delay: 0.05 * i }}
                    >
                      <span className={styles.hintNum}>0{i + 1}</span>
                      <p className={styles.hintText}>{hint.text}</p>
                    </motion.div>
                  ) : (
                    <motion.div key={`hidden-${i}`} className={styles.hintHidden}>
                      <span className={styles.hintNum}>0{i + 1}</span>
                      <p className={styles.hintHiddenText}>
                        Classified clue unlocks at {i === 0 ? '0:30' : i === 1 ? '1:00' : '1:30'}
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
              );
            })}
          </div>
        </div>
      </main>

      {/* Footer Branding */}
      <footer className={styles.footerBar}>
        <span>OPEN MINDS CLUB PRESENTS · THE ANIME HUNTER EXAM</span>
      </footer>
    </div>
  );
}
