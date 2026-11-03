import React from 'react';
import type { AnimeUniverse } from '../../types';
import styles from './SpiderWebBackground.module.css';

export interface SpiderWebBackgroundProps {
  universe?: AnimeUniverse | 'movies' | string | null;
  className?: string;
  intensity?: 'subtle' | 'normal' | 'vivid';
}

interface ThemeConfig {
  id: string;
  image: string;
  character: string;
  themeTitle: string;
  accent: string;
  glow: string;
  rgb: string;
}

const UNIVERSE_THEMES: Record<string, ThemeConfig> = {
  'hunter-x-hunter': {
    id: 'hunter-x-hunter',
    image: '/assets/backgrounds/bg_hxh.jpg',
    character: 'GON FREECSS & KILLUA ZOLDYCK',
    themeTitle: 'HUNTER ASSOCIATION • 287TH EXAM',
    accent: '#4ADE80',
    glow: 'rgba(74, 222, 128, 0.28)',
    rgb: '74, 222, 128',
  },
  'naruto': {
    id: 'naruto',
    image: '/assets/backgrounds/bg_naruto.jpg',
    character: 'NARUTO UZUMAKI • KURAMA CHAKRA',
    themeTitle: 'HIDDEN LEAF • CHUNIN SELECTION',
    accent: '#F97316',
    glow: 'rgba(249, 115, 22, 0.28)',
    rgb: '249, 115, 22',
  },
  'jujutsu-kaisen': {
    id: 'jujutsu-kaisen',
    image: '/assets/backgrounds/bg_jjk.jpg',
    character: 'GOJO SATORU • HOLLOW PURPLE',
    themeTitle: 'TOKYO JUJUTSU HIGH • SPECIAL GRADE',
    accent: '#A855F7',
    glow: 'rgba(168, 85, 247, 0.28)',
    rgb: '168, 85, 247',
  },
  'one-piece': {
    id: 'one-piece',
    image: '/assets/backgrounds/bg_one-piece.jpg',
    character: 'MONKEY D. LUFFY • GEAR 5 SUN GOD',
    themeTitle: 'GRAND LINE • PIRATE KING TRIAL',
    accent: '#EAB308',
    glow: 'rgba(234, 179, 8, 0.28)',
    rgb: '234, 179, 8',
  },
  'marvel': {
    id: 'marvel',
    image: '/assets/backgrounds/bg_marvel.jpg',
    character: 'CYBER ARMORED AVENGERS HERO',
    themeTitle: 'EARTH-616 • MULTIVERSE INITIATIVE',
    accent: '#EF4444',
    glow: 'rgba(239, 68, 68, 0.28)',
    rgb: '239, 68, 68',
  },
  'football': {
    id: 'football',
    image: '/assets/backgrounds/bg_football.jpg',
    character: 'NUMBER 10 MAESTRO • BALLON D\'OR',
    themeTitle: 'ESTADIO MONUMENTAL • WORLD CUP LEGENDS',
    accent: '#10B981',
    glow: 'rgba(16, 185, 129, 0.28)',
    rgb: '16, 185, 129',
  },
  'movies': {
    id: 'movies',
    image: '/assets/backgrounds/bg_movies.jpg',
    character: 'CINEMA MYSTERY • CELLULOID NOIR',
    themeTitle: 'GRAND CINÉMA • 30 ICONIC MASTERPIECES',
    accent: '#F43F5E',
    glow: 'rgba(244, 63, 94, 0.32)',
    rgb: '244, 63, 94',
  },
};

export const SpiderWebBackground: React.FC<SpiderWebBackgroundProps> = ({
  universe = 'hunter-x-hunter',
  className = '',
  intensity = 'normal',
}) => {
  const activeKey = (universe && UNIVERSE_THEMES[universe]) ? universe : 'hunter-x-hunter';
  const currentTheme = UNIVERSE_THEMES[activeKey];

  return (
    <div
      className={`${styles.container} ${styles[intensity]} ${className}`}
      style={{
        '--active-accent': currentTheme.accent,
        '--active-glow': currentTheme.glow,
        '--active-rgb': currentTheme.rgb,
      } as React.CSSProperties}
      aria-hidden="true"
    >
      {/* ── 1. Base Dark Canvas ─────────────────────────── */}
      <div className={styles.baseCanvas} />

      {/* ── 2. Cinematic Character Wallpaper Cross-Fades ─── */}
      <div className={styles.wallpapersStack}>
        {Object.values(UNIVERSE_THEMES).map((theme) => {
          const isActive = theme.id === activeKey;
          return (
            <div
              key={theme.id}
              className={`${styles.wallpaperItem} ${isActive ? styles.wallpaperActive : ''}`}
            >
              <img
                src={theme.image}
                alt={theme.character}
                className={styles.wallpaperImg}
                loading="eager"
              />
            </div>
          );
        })}
      </div>

      {/* ── 3. Dynamic Topic Nen Aura & Color Wash ────────── */}
      <div className={styles.nenAuraGlow} />

      {/* ── 4. Atmospheric Vignette Overlay ───────────────── */}
      <div className={styles.vignetteOverlay} />

      {/* ── 5. Floating Nen / Energy Sparks ───────────────── */}
      <div className={styles.sparksContainer}>
        <div className={`${styles.spark} ${styles.s1}`} />
        <div className={`${styles.spark} ${styles.s2}`} />
        <div className={`${styles.spark} ${styles.s3}`} />
        <div className={`${styles.spark} ${styles.s4}`} />
        <div className={`${styles.spark} ${styles.s5}`} />
        <div className={`${styles.spark} ${styles.s6}`} />
      </div>

      {/* ── 6. Hunter Exam Spiderweb Overlay ──────────────── */}
      <svg
        className={styles.webSvg}
        viewBox="0 0 1440 900"
        preserveAspectRatio="xMidYMid slice"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id="webDynamicGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="var(--active-accent)" stopOpacity="0.35" />
            <stop offset="50%" stopColor="#ffffff" stopOpacity="0.12" />
            <stop offset="100%" stopColor="var(--active-accent)" stopOpacity="0.05" />
          </linearGradient>
        </defs>

        {/* Primary Hunter Spiderweb */}
        <g stroke="url(#webDynamicGrad)" strokeWidth="1.1" strokeLinecap="round">
          <line x1="180" y1="220" x2="-40" y2="10" />
          <line x1="180" y1="220" x2="40" y2="-40" />
          <line x1="180" y1="220" x2="180" y2="-60" />
          <line x1="180" y1="220" x2="340" y2="-30" />
          <line x1="180" y1="220" x2="480" y2="30" />
          <line x1="180" y1="220" x2="560" y2="160" />
          <line x1="180" y1="220" x2="540" y2="320" />
          <line x1="180" y1="220" x2="440" y2="440" />
          <line x1="180" y1="220" x2="280" y2="520" />
          <line x1="180" y1="220" x2="120" y2="540" />
          <line x1="180" y1="220" x2="-20" y2="460" />
          <line x1="180" y1="220" x2="-80" y2="320" />

          {/* Web Spiral Arc 1 */}
          <path d="M 120 180 Q 150 150 180 150 Q 220 150 250 170 Q 280 200 280 230 Q 270 270 240 290 Q 200 310 160 300 Q 120 280 110 240 Z" />
          {/* Web Spiral Arc 2 */}
          <path d="M 60 140 Q 120 80 180 80 Q 270 80 330 120 Q 380 170 380 240 Q 360 330 300 380 Q 220 420 130 390 Q 50 350 40 270 Z" />
          {/* Web Spiral Arc 3 */}
          <path d="M -20 80 Q 80 -10 180 -10 Q 330 -10 420 60 Q 500 140 490 260 Q 460 390 370 470 Q 240 540 100 500 Q -20 430 -40 310 Z" />
        </g>
      </svg>

      {/* ── 7. Atmospheric HUD Watermark (Bottom Right) ──── */}
      <aside className={styles.hudBadge} aria-hidden="true">
        <span className={styles.hudPulseDot} />
        <span className={styles.hudChar}>{currentTheme.character}</span>
        <span className={styles.hudSeparator}>•</span>
        <span className={styles.hudTitle}>{currentTheme.themeTitle}</span>
      </aside>
    </div>
  );
};
