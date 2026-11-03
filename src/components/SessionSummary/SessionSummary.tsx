import { motion } from 'framer-motion';
import { Trophy, CheckCircle, XCircle, RotateCcw, Home, Award, Star, User } from 'lucide-react';
import type { GameSession, AnimeUniverse } from '../../types';
import { ANIME_META } from '../../types';
import { getPrefs } from '../../services/storageService';
import styles from './SessionSummary.module.css';

interface Props {
  session: GameSession;
  onReplay: () => void;
  onHome: () => void;
  onLeaderboard: () => void;
}

export default function SessionSummary({ session, onReplay, onHome, onLeaderboard }: Props) {
  const meta = ANIME_META[session.anime as AnimeUniverse];
  const prefs = getPrefs();
  const candidateName = prefs.nickname && prefs.nickname !== 'Hunter' ? prefs.nickname : 'Examinee';
  const correct = session.rounds.filter(r => r.isCorrect).length;
  const total = session.rounds.length;
  const accuracy = total > 0 ? Math.round((correct / total) * 100) : 0;
  const bestTime = correct > 0
    ? Math.min(...session.rounds.filter(r => r.isCorrect).map(r => r.timeElapsed))
    : 0;
  const bMins = Math.floor(bestTime / 60);
  const bSecs = bestTime % 60;

  return (
    <motion.div
      className={styles.page}
      style={{ '--accent': meta.accent, '--glow': meta.glow } as React.CSSProperties}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      {/* Header */}
      <header className={styles.header}>
        <Trophy size={32} className={styles.headerIcon} />
        <h1 className={styles.headerTitle}>EXAM COMPLETE</h1>
        <p className={styles.headerSub}>{meta.examLabel}</p>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          background: 'rgba(255, 255, 255, 0.05)',
          border: '1px solid var(--accent)',
          padding: '4px 14px',
          borderRadius: '999px',
          fontSize: '11px',
          letterSpacing: '1.5px',
          color: 'var(--text-secondary)',
          marginTop: '8px'
        }}>
          <User size={13} style={{ color: 'var(--accent)' }} />
          <span>Examinee: <strong style={{ color: '#FFF' }}>{candidateName}</strong> (Tag #404) • Recorded to Leaderboard</span>
        </div>
      </header>

      {/* Score hero */}
      <div className={styles.scoreHero}>
        <div className={styles.scoreCircle}>
          <span className={styles.scoreVal}>{session.totalScore}</span>
          <span className={styles.scoreLabel}>POINTS</span>
        </div>
      </div>

      {/* Stats row */}
      <div className={styles.statsRow}>
        <div className={styles.stat}>
          <CheckCircle size={18} className={styles.statIconCorrect} />
          <span className={styles.statVal}>{correct} / {total}</span>
          <span className={styles.statKey}>CORRECT</span>
        </div>
        <div className={styles.stat}>
          <Star size={18} className={styles.statIconAccent} />
          <span className={styles.statVal}>{accuracy}%</span>
          <span className={styles.statKey}>ACCURACY</span>
        </div>
        <div className={styles.stat}>
          <Award size={18} className={styles.statIconAccent} />
          <span className={styles.statVal}>
            {correct > 0 ? `${String(bMins).padStart(2,'0')}:${String(bSecs).padStart(2,'0')}` : '--'}
          </span>
          <span className={styles.statKey}>BEST TIME</span>
        </div>
      </div>

      {/* Round list */}
      <div className={styles.roundList}>
        <p className={styles.roundListTitle}>ROUND BREAKDOWN</p>
        {session.rounds.map((r, i) => (
          <div key={i} className={`${styles.roundRow} ${r.isCorrect ? styles.rowCorrect : styles.rowWrong}`}>
            <span className={styles.roundNum}>#{i + 1}</span>
            <div className={styles.roundInfo}>
              <span className={styles.roundChar}>{r.character.name}</span>
              <span className={styles.roundMeta}>
                {r.isCorrect
                  ? `${r.timeElapsed}s · ${r.hintsRevealed} hints`
                  : 'Timed out'}
              </span>
            </div>
            <div className={styles.roundResult}>
              {r.isCorrect
                ? <><CheckCircle size={14} /> <span>+{r.pointsEarned}</span></>
                : <><XCircle size={14} /> <span>0</span></>
              }
            </div>
          </div>
        ))}
      </div>

      {/* Actions */}
      <div className={styles.actions}>
        <motion.button className={styles.btnPrimary} onClick={onReplay}
          whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
          <RotateCcw size={16} /> PLAY AGAIN
        </motion.button>
        <button className={styles.btnSecondary} onClick={onLeaderboard}>
          <Trophy size={14} /> LEADERBOARD
        </button>
        <button className={styles.btnSecondary} onClick={onHome}>
          <Home size={14} /> HOME
        </button>
      </div>
    </motion.div>
  );
}
