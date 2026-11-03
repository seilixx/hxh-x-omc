import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { SpiderWebBackground } from '../common/SpiderWebBackground';
import { HxhOmcBrandHeader } from '../brand/HxhOmcBrandHeader';
import styles from './LoadingScreen.module.css';

interface Props {
  onComplete: () => void;
}

export default function LoadingScreen({ onComplete }: Props) {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timings = [500, 1200, 2200, 3200];
    const timers = timings.map((t, i) =>
      setTimeout(() => setPhase(i + 1), t)
    );
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <motion.div
      className={styles.overlay}
      initial={{ opacity: 1 }}
      exit={{ opacity: 0, transition: { duration: 0.8, ease: 'easeInOut' } }}
    >
      {/* Spiderweb Background from Reference Image */}
      <SpiderWebBackground />

      {/* Center Cinematic Brand Composition */}
      <div className={styles.centerStage}>
        <AnimatePresence>
          {phase >= 1 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1, ease: 'easeOut' }}
              className={styles.brandWrapper}
            >
              {/* Exact Dual Logo Lockup with Spiders Dangling */}
              <HxhOmcBrandHeader
                size="large"
                subtitle="THE ANIME HUNTER EXAM • OPEN MINDS CLUB"
                showSubtitle={phase >= 2}
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Cinematic Title & Exam Badge */}
        <AnimatePresence>
          {phase >= 2 && (
            <motion.div
              className={styles.titleGroup}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className={styles.examTitle}>WHO AM I?</h1>
              <p className={styles.examSub}>
                HUNTER ASSOCIATION SPECIAL EXAMINATION COMMISSION
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Progress Bar & Status */}
        <AnimatePresence>
          {phase >= 3 && (
            <motion.div
              className={styles.progressSection}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6 }}
            >
              <div className={styles.progressTrack}>
                <motion.div
                  className={styles.progressBar}
                  initial={{ width: '0%' }}
                  animate={{ width: '100%' }}
                  transition={{ duration: 1.0, ease: 'easeInOut' }}
                  onAnimationComplete={onComplete}
                />
              </div>
              <div className={styles.statusRow}>
                <span className={styles.statusCode}>EXAM_INITIALIZING</span>
                <span className={styles.statusNen}>NEN VERIFICATION COMPLETE</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Skip Button */}
      <button className={styles.skipBtn} onClick={onComplete}>
        SKIP INTRO [ESC] →
      </button>
    </motion.div>
  );
}
