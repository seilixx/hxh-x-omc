import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, Clock, Lightbulb, Star, ArrowRight, RotateCcw, Home, StopCircle, Eye } from 'lucide-react';
import type { AnimeUniverse, RoundResult, GameMode } from '../../types';
import { ANIME_META } from '../../types';
import styles from './ResultScreen.module.css';

interface Props {
  result: RoundResult;
  anime: AnimeUniverse;
  totalScore: number;
  roundNumber: number;
  totalRounds: number | null;
  mode: GameMode;
  onNext: () => void;
  onReplay: () => void;
  onHome: () => void;
  onEndSession?: () => void;
}

export default function ResultScreen({
  result,
  anime,
  totalScore,
  roundNumber,
  totalRounds,
  mode,
  onNext,
  onReplay,
  onHome,
  onEndSession,
}: Props) {
  const meta = ANIME_META[anime];
  const { character, isCorrect, timeElapsed, hintsRevealed, pointsEarned } = result;

  const mins = Math.floor(timeElapsed / 60);
  const secs = timeElapsed % 60;
  const timeStr = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  const [imgError, setImgError] = useState(false);

  // Auto-next countdown for Endless mode
  const [autoNextSeconds, setAutoNextSeconds] = useState(mode === 'endless' ? 6 : null);

  useEffect(() => {
    if (autoNextSeconds === null) return;
    if (autoNextSeconds <= 0) {
      onNext();
      return;
    }
    const timer = setTimeout(() => {
      setAutoNextSeconds(s => (s !== null ? s - 1 : null));
    }, 1000);
    return () => clearTimeout(timer);
  }, [autoNextSeconds, onNext]);

  return (
    <motion.div
      className={styles.page}
      style={{ '--accent': meta.accent, '--glow': meta.glow } as React.CSSProperties}
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
    >
      {/* Result banner */}
      <div className={`${styles.banner} ${isCorrect ? styles.bannerCorrect : styles.bannerTimeout}`}>
        <div className={styles.bannerIcon}>
          {isCorrect ? <CheckCircle size={28} /> : <XCircle size={28} />}
        </div>
        <div>
          <p className={styles.bannerLabel}>
            {isCorrect ? 'CANDIDATE IDENTIFIED' : "TIME EXPIRED — UNIDENTIFIED"}
          </p>
          <p className={styles.bannerPoints}>
            {isCorrect ? `+${pointsEarned} POINTS AWARDED` : '0 POINTS AWARDED'}
          </p>
        </div>
        {mode === 'endless' && autoNextSeconds !== null && (
          <div className={styles.autoAdvanceBadge}>
            <span>AUTO ADVANCE IN {autoNextSeconds}S</span>
            <button
              className={styles.cancelAutoBtn}
              onClick={() => setAutoNextSeconds(null)}
            >
              PAUSE
            </button>
          </div>
        )}
      </div>

      {/* Content */}
      <div className={styles.content}>
        {/* Portrait Column */}
        <div className={styles.portraitCol}>
          <div className={styles.portrait}>
            {imgError ? (
              <div className={styles.fallbackSilhouette}>
                <span className={styles.fallbackInitials}>
                  {character.name.slice(0, 2).toUpperCase()}
                </span>
                <span className={styles.fallbackId}>#{character.id.toUpperCase()}</span>
              </div>
            ) : (
              <img
                src={character.image}
                alt={character.name}
                className={styles.charImg}
                referrerPolicy="no-referrer"
                crossOrigin="anonymous"
                onError={() => setImgError(true)}
              />
            )}
            <div className={styles.portraitOverlay} />
            <div className={styles.charNameBadge}>
              <span className={styles.charUniverseTag}>{meta.label}</span>
              <h2 className={styles.charName}>{character.name}</h2>
            </div>
          </div>
        </div>

        {/* Stats + Dossier Info Column */}
        <div className={styles.infoCol}>
          {/* Character Dossier Card */}
          <div className={styles.card}>
            <h3 className={styles.cardTitle}>CANDIDATE DOSSIER</h3>
            <div className={styles.charInfo}>
              <div className={styles.infoRow}>
                <span className={styles.infoKey}>CANON NAME</span>
                <span className={styles.infoVal}>{character.name}</span>
              </div>
              {character.aliases.length > 0 && (
                <div className={styles.infoRow}>
                  <span className={styles.infoKey}>KNOWN ALIASES</span>
                  <span className={styles.infoVal}>{character.aliases.join(', ')}</span>
                </div>
              )}
              {character.affiliation && (
                <div className={styles.infoRow}>
                  <span className={styles.infoKey}>AFFILIATION</span>
                  <span className={styles.infoVal}>{character.affiliation}</span>
                </div>
              )}
              {character.arc && (
                <div className={styles.infoRow}>
                  <span className={styles.infoKey}>FIRST APPEARANCE</span>
                  <span className={styles.infoVal}>{character.arc}</span>
                </div>
              )}
              {character.nenType && (
                <div className={styles.infoRow}>
                  <span className={styles.infoKey}>NEN TYPE</span>
                  <span className={styles.infoVal}>{character.nenType}</span>
                </div>
              )}
              {character.rank && (
                <div className={styles.infoRow}>
                  <span className={styles.infoKey}>SHINOBI RANK</span>
                  <span className={styles.infoVal}>{character.rank}</span>
                </div>
              )}
              {character.crew && (
                <div className={styles.infoRow}>
                  <span className={styles.infoKey}>PIRATE CREW</span>
                  <span className={styles.infoVal}>{character.crew}</span>
                </div>
              )}
              {character.school && (
                <div className={styles.infoRow}>
                  <span className={styles.infoKey}>JUJUTSU SCHOOL</span>
                  <span className={styles.infoVal}>{character.school}</span>
                </div>
              )}
              <div className={styles.infoRow}>
                <span className={styles.infoKey}>EXAM DIFFICULTY</span>
                <span className={styles.infoVal} data-diff={character.difficulty}>
                  {character.difficulty.toUpperCase()}
                </span>
              </div>
            </div>
            <p className={styles.charDesc}>{character.description}</p>
          </div>

          {/* Dossier Hints Revealed */}
          <div className={styles.hintsReview}>
            <p className={styles.hintsReviewTitle}>
              <Eye size={12} />
              EXAMINER'S DOSSIER HINTS:
            </p>
            <div className={styles.hintsList}>
              {character.hints.map((h, i) => (
                <div key={i} className={styles.hintItem}>
                  <span className={styles.hintBadge}>CLUE {i + 1}</span>
                  <span className={styles.hintText}>{h.text}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Round Stats */}
          <div className={styles.statsGrid}>
            <div className={styles.stat}>
              <Clock size={16} className={styles.statIcon} />
              <span className={styles.statVal}>{timeStr}</span>
              <span className={styles.statKey}>TIME TAKEN</span>
            </div>
            <div className={styles.stat}>
              <Lightbulb size={16} className={styles.statIcon} />
              <span className={styles.statVal}>{hintsRevealed} / 3</span>
              <span className={styles.statKey}>HINTS UNLOCKED</span>
            </div>
            <div className={styles.stat}>
              <Star size={16} className={styles.statIcon} />
              <span className={styles.statVal}>+{pointsEarned}</span>
              <span className={styles.statKey}>SCORE GAINED</span>
            </div>
          </div>

          {/* Total Accumulated Score */}
          <div className={styles.totalScore}>
            <span className={styles.totalLabel}>TOTAL EXAM SCORE</span>
            <span className={styles.totalVal}>{totalScore}</span>
          </div>

          {/* Action Buttons */}
          <div className={styles.actions}>
            <motion.button
              className={styles.btnPrimary}
              onClick={onNext}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <ArrowRight size={16} />
              {totalRounds && roundNumber >= totalRounds ? 'COMPLETE EXAM & SEE SUMMARY' : 'NEXT CHARACTER ›'}
            </motion.button>

            <div className={styles.secondaryBtns}>
              {mode === 'endless' && onEndSession && (
                <button className={styles.btnEndSession} onClick={onEndSession}>
                  <StopCircle size={14} /> END EXAM SESSION
                </button>
              )}
              <button className={styles.btnSecondary} onClick={onReplay}>
                <RotateCcw size={14} /> REPLAY EXAM
              </button>
              <button className={styles.btnSecondary} onClick={onHome}>
                <Home size={14} /> RETURN TO ANIME SELECTION
              </button>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
