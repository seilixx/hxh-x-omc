import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Shield, Sparkles } from 'lucide-react';
import type { Character, AnimeUniverse } from '../../types';
import { ANIME_META } from '../../types';
import styles from './CharacterPortrait.module.css';

interface Props {
  character: Character;
  anime: AnimeUniverse;
  blur: number;
  isRevealed: boolean;
  roundStatus: 'playing' | 'correct' | 'timeout';
}

export default function CharacterPortrait({
  character,
  anime,
  blur,
  isRevealed,
  roundStatus,
}: Props) {
  const [imgError, setImgError] = useState(false);
  const meta = ANIME_META[anime];

  // Reset image error state when character changes
  useEffect(() => {
    setImgError(false);
  }, [character.id]);

  // Derive candidate initials
  const initials = character.name
    .split(' ')
    .slice(0, 2)
    .map(w => w[0])
    .join('')
    .toUpperCase();

  return (
    <div className={styles.wrap} style={{ '--accent': meta.accent, '--glow': meta.glow } as React.CSSProperties}>
      <motion.div
        key={character.id}
        className={`${styles.portrait} ${roundStatus === 'correct' ? styles.correctGlow : ''}`}
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
      >
        {imgError ? (
          /* High-aesthetic procedural silhouette placeholder when image fails */
          <div
            className={styles.silhouetteCard}
            style={{ filter: `blur(${blur}px)` }}
          >
            <div className={styles.silhouetteAura} />
            <div className={styles.cardWatermark}>
              <Shield size={120} strokeWidth={1} />
            </div>
            
            {/* Candidate avatar silhouette */}
            <div className={styles.avatarShape}>
              <div className={styles.avatarHead} />
              <div className={styles.avatarShoulders} />
              <span className={styles.avatarInitials}>{initials}</span>
            </div>

            <div className={styles.silhouetteMeta}>
              <span className={styles.candidateId}>EXAM ID #{character.id.toUpperCase()}</span>
              {character.arc && <span className={styles.candidateArc}>{character.arc}</span>}
              {character.nenType && <span className={styles.candidateNen}>NEN: {character.nenType}</span>}
            </div>
          </div>
        ) : (
          <img
            src={character.image}
            alt={isRevealed ? character.name : 'Target candidate portrait'}
            className={styles.img}
            style={{ filter: `blur(${blur}px)` }}
            referrerPolicy="no-referrer"
            crossOrigin="anonymous"
            onError={() => setImgError(true)}
          />
        )}

        {/* Ambient shadow gradient */}
        {!isRevealed && <div className={styles.darkGradient} />}

        {/* Hunter Association Watermark */}
        <div className={styles.associationStamp}>
          <span className={styles.stampText}>HUNTER EXAM · TARGET RECORD</span>
        </div>

        {/* Correct Reveal Overlay */}
        {roundStatus === 'correct' && (
          <motion.div
            className={styles.correctOverlay}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className={styles.correctTag}>
              <Sparkles size={14} /> IDENTIFIED
            </div>
            <h2 className={styles.correctName}>{character.name}</h2>
          </motion.div>
        )}

        {/* Timeout Overlay */}
        {roundStatus === 'timeout' && (
          <motion.div
            className={styles.timeoutOverlay}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className={styles.timeoutTag}>TIME EXPIRED</div>
            <h2 className={styles.timeoutName}>{character.name}</h2>
          </motion.div>
        )}
      </motion.div>

      {/* Difficulty Stamp */}
      <div className={styles.diffBadge} data-diff={character.difficulty}>
        {character.difficulty.toUpperCase()}
      </div>
    </div>
  );
}
