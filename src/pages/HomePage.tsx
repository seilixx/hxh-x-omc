import { useState } from 'react';
import { motion } from 'framer-motion';
import type { Variants } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Trophy, User, ArrowRight, Film, Sparkles, Compass, Shield, Flame, Zap, Award, Film as CinemaIcon } from 'lucide-react';
import type { AnimeUniverse } from '../types';
import { SpiderWebBackground } from '../components/common/SpiderWebBackground';
import { HxhOmcBrandHeader } from '../components/brand/HxhOmcBrandHeader';
import { getPrefs } from '../services/storageService';
import styles from './HomePage.module.css';

type SectionCategory = 'all' | 'anime' | 'pop-culture' | 'cinema';

interface UniverseItem {
  id: AnimeUniverse | 'movies';
  category: 'anime' | 'pop-culture' | 'cinema';
  label: string;
  tagline: string;
  description: string;
  accent: string;
  glow: string;
  rgb: string;
  bg: string;
  path: string;
  isMain?: boolean;
  characterTitle: string;
  characterIcon: React.ReactNode;
  candidateCount: string;
  difficultyBadge: string;
}

const UNIVERSES: UniverseItem[] = [
  {
    id: 'hunter-x-hunter',
    category: 'anime',
    label: 'HUNTER × HUNTER',
    tagline: 'MAIN EXAM • ASSOCIATION',
    description: 'Enter the Hunter Association universe. Face 50 canon candidates from the 287th Exam to the Chimera Ant arc.',
    accent: '#4ADE80',
    glow: 'rgba(74, 222, 128, 0.35)',
    rgb: '74, 222, 128',
    bg: '/assets/backgrounds/bg_hxh.jpg',
    path: '/game/hunter-x-hunter',
    isMain: true,
    characterTitle: 'Gon & Killua (Nen Aura)',
    characterIcon: <Zap size={14} />,
    candidateCount: '50 CANDIDATES',
    difficultyBadge: 'NEN MASTERY',
  },
  {
    id: 'naruto',
    category: 'anime',
    label: 'NARUTO SHINOBI',
    tagline: 'CHUNIN SELECTION TRIAL',
    description: 'Master the shinobi arts. From Hidden Leaf prodigies and legendary Sannin to the formidable Akatsuki rogues.',
    accent: '#F97316',
    glow: 'rgba(249, 115, 22, 0.35)',
    rgb: '249, 115, 22',
    bg: '/assets/backgrounds/bg_naruto.jpg',
    path: '/game/naruto',
    characterTitle: 'Naruto & Kurama Chakra',
    characterIcon: <Flame size={14} />,
    candidateCount: '50 SHINOBI',
    difficultyBadge: 'CHUNIN TO KAGE',
  },
  {
    id: 'jujutsu-kaisen',
    category: 'anime',
    label: 'JUJUTSU KAISEN',
    tagline: 'CURSED ENERGY TRIAL',
    description: 'Enter the jujutsu sorcery realm. Identify special grade sorcerers, lethal cursed spirits, and historical reincarnations.',
    accent: '#A855F7',
    glow: 'rgba(168, 85, 247, 0.35)',
    rgb: '168, 85, 247',
    bg: '/assets/backgrounds/bg_jjk.jpg',
    path: '/game/jujutsu-kaisen',
    characterTitle: 'Gojo Satoru (Domain)',
    characterIcon: <Sparkles size={14} />,
    candidateCount: '50 SORCERERS',
    difficultyBadge: 'SPECIAL GRADE',
  },
  {
    id: 'one-piece',
    category: 'anime',
    label: 'ONE PIECE',
    tagline: 'GRAND LINE EXAM',
    description: 'Sail the Grand Line and prove your pirate mastery. From East Blue rookies to the Four Emperors and Marines.',
    accent: '#EAB308',
    glow: 'rgba(234, 179, 8, 0.35)',
    rgb: '234, 179, 8',
    bg: '/assets/backgrounds/bg_one-piece.jpg',
    path: '/game/one-piece',
    characterTitle: 'Luffy Gear 5 Sun God',
    characterIcon: <Sparkles size={14} />,
    candidateCount: '50 PIRATES',
    difficultyBadge: 'PIRATE KING TRIAL',
  },
  {
    id: 'marvel',
    category: 'pop-culture',
    label: 'MARVEL UNIVERSE',
    tagline: 'AVENGERS INITIATIVE',
    description: 'Earth-616 to the cosmos. Earth\'s mightiest champions, tech geniuses, galactic rogues, and cosmic warlords.',
    accent: '#EF4444',
    glow: 'rgba(239, 68, 68, 0.35)',
    rgb: '239, 68, 68',
    bg: '/assets/backgrounds/bg_marvel.jpg',
    path: '/game/marvel',
    characterTitle: 'Cyber Armored Avenger',
    characterIcon: <Shield size={14} />,
    candidateCount: '50 HEROES',
    difficultyBadge: 'STREET TO COSMIC',
  },
  {
    id: 'football',
    category: 'pop-culture',
    label: 'WORLD FOOTBALL',
    tagline: 'BALLON D\'OR LEGENDS',
    description: 'Legends of the world\'s game. World Cup champions, UEFA masters, record holders, and footballing deities.',
    accent: '#10B981',
    glow: 'rgba(16, 185, 129, 0.35)',
    rgb: '16, 185, 129',
    bg: '/assets/backgrounds/bg_football.jpg',
    path: '/game/football',
    characterTitle: 'Number 10 Maestro',
    characterIcon: <Award size={14} />,
    candidateCount: '50 MAESTROS',
    difficultyBadge: 'BALLON D\'OR TIER',
  },
  {
    id: 'movies',
    category: 'cinema',
    label: 'GUESS THE MOVIE',
    tagline: 'PURE HINTS • NO PHOTOS',
    description: 'The ultimate cinema deduction test. Deduce iconic films strictly through directors, quotes, cast, and plot clues.',
    accent: '#F43F5E',
    glow: 'rgba(244, 63, 94, 0.4)',
    rgb: '244, 63, 94',
    bg: '/assets/backgrounds/bg_movies.jpg',
    path: '/movies',
    characterTitle: 'Cinema Noir Projector',
    characterIcon: <CinemaIcon size={14} />,
    candidateCount: '30 MASTERPIECES',
    difficultyBadge: 'PLOT & QUOTES ONLY',
  },
];

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08 } },
};

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] } },
};

export default function HomePage() {
  const navigate = useNavigate();
  const prefs = getPrefs();
  const candidateName = prefs.nickname && prefs.nickname !== 'Hunter' ? prefs.nickname : null;
  const [selectedCategory, setSelectedCategory] = useState<SectionCategory>('all');
  const [hoveredUniverse, setHoveredUniverse] = useState<AnimeUniverse | 'movies' | null>(null);
  const [selectedUniverse, setSelectedUniverse] = useState<AnimeUniverse | 'movies'>('hunter-x-hunter');

  const visibleUniverses = selectedCategory === 'all'
    ? UNIVERSES
    : UNIVERSES.filter(u => u.category === selectedCategory);

  // Active theme for dynamic character background
  const currentBackgroundUniverse = hoveredUniverse || selectedUniverse;

  return (
    <div className={styles.page}>
      {/* Dynamic Universe Background inspired by HxH & Anime Characters */}
      <SpiderWebBackground universe={currentBackgroundUniverse} />

      {/* Navigation Bar */}
      <nav className={styles.nav}>
        <div className={styles.navBrand}>
          <img
            src="/assets/logos/Open Minds Logo.svg"
            alt="Open Minds Club"
            className={styles.navLogoImg}
          />
          <div className={styles.navDivider} />
          <div className={styles.navCollabBox}>
            <span className={styles.navCollabHxh}>HUNTER × HUNTER</span>
            <span className={styles.navTitle}>THE POP CULTURE & ANIME EXAM</span>
          </div>
        </div>

        <div className={styles.navActions}>
          {candidateName && (
            <div className={styles.candidateBadgePreview}>
              <User size={13} className={styles.candidateIcon} />
              <span className={styles.candidateText}>Examinee: <strong>{candidateName}</strong></span>
            </div>
          )}
          <button className={styles.navBtn} onClick={() => navigate('/leaderboard')}>
            <Trophy size={14} />
            LEADERBOARD
          </button>
        </div>
      </nav>

      {/* Hero Section with Official Brand Header & Spiders */}
      <motion.header
        className={styles.hero}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        {/* Exact Logo Lockup + Hanging Spiders */}
        <HxhOmcBrandHeader
          size="large"
          subtitle="HUNTER ASSOCIATION × OPEN MINDS CLUB • WHO AM I?"
          showSubtitle={true}
        />

        <div className={styles.heroTextGroup}>
          <h1 className={styles.heroTitle}>WHO AM I?</h1>
          <p className={styles.heroSub}>
            Machine vs Human identification challenge. Hover or select any exam to preview its signature character atmosphere, then prove your mastery across Shonen Anime, Marvel, World Football, and Cinema Mystery.
          </p>
        </div>

        <div className={styles.heroDivider} />
      </motion.header>

      {/* Category Tabs */}
      <div className={styles.categoryTabs}>
        <button
          className={`${styles.categoryTab} ${selectedCategory === 'all' ? styles.categoryTabActive : ''}`}
          onClick={() => setSelectedCategory('all')}
        >
          <Compass size={14} /> ALL CHALLENGES (7)
        </button>
        <button
          className={`${styles.categoryTab} ${selectedCategory === 'anime' ? styles.categoryTabActive : ''}`}
          onClick={() => setSelectedCategory('anime')}
        >
          <Sparkles size={14} /> SHONEN ANIME (4)
        </button>
        <button
          className={`${styles.categoryTab} ${selectedCategory === 'pop-culture' ? styles.categoryTabActive : ''}`}
          onClick={() => setSelectedCategory('pop-culture')}
        >
          <Trophy size={14} /> POP CULTURE & FOOTBALL (2)
        </button>
        <button
          className={`${styles.categoryTab} ${selectedCategory === 'cinema' ? styles.categoryTabActive : ''}`}
          style={selectedCategory === 'cinema' ? { borderColor: '#F43F5E', color: '#F43F5E', boxShadow: '0 0 16px rgba(244, 63, 94, 0.3)' } : {}}
          onClick={() => setSelectedCategory('cinema')}
        >
          <Film size={14} /> CINEMA: GUESS THE MOVIE (NEW)
        </button>
      </div>

      {/* Universe Selection Grid */}
      <motion.main
        key={selectedCategory}
        className={styles.grid}
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {visibleUniverses.map((item) => {
          const isSelected = selectedUniverse === item.id;
          const isHovered = hoveredUniverse === item.id;

          return (
            <motion.article
              key={item.id}
              className={`${styles.card} ${item.isMain ? styles.cardMain : ''} ${isSelected ? styles.cardSelected : ''}`}
              style={{
                '--accent': item.accent,
                '--glow': item.glow,
                '--rgb': item.rgb,
              } as React.CSSProperties}
              variants={cardVariants}
              whileHover={{ y: -8, scale: 1.015, transition: { duration: 0.25 } }}
              onClick={() => {
                setSelectedUniverse(item.id);
                navigate(item.path);
              }}
              onMouseEnter={() => setHoveredUniverse(item.id)}
              onMouseLeave={() => setHoveredUniverse(null)}
              onFocus={() => setHoveredUniverse(item.id)}
              onBlur={() => setHoveredUniverse(null)}
              role="button"
              tabIndex={0}
              onKeyDown={e => e.key === 'Enter' && navigate(item.path)}
              aria-label={`Select ${item.label} exam`}
            >
              {/* Tactical Aura Rim Lighting */}
              <div className={styles.cardAuraBorder} />

              {/* Background character art with high-contrast vignette */}
              <div className={styles.cardBg}>
                <img
                  src={item.bg}
                  alt={item.label}
                  className={styles.cardImg}
                  onError={e => { (e.target as HTMLImageElement).style.display = 'none'; }}
                />
                <div className={styles.cardOverlay} />
                <div className={styles.cardInnerGlow} />
              </div>

              {/* Top Header Badges */}
              <div className={styles.cardTopHeader}>
                <div className={styles.cardTopLeft}>
                  {item.isMain && <span className={styles.mainBadge}>★ OFFICIAL EXAM</span>}
                  {item.id === 'movies' && <span className={styles.cinemaHighlightBadge}>🎬 NO PHOTOS • HINTS ONLY</span>}
                  <span className={styles.categoryBadge}>{item.category.toUpperCase()}</span>
                </div>
                <div className={styles.candidateCounterBadge}>
                  {item.candidateCount}
                </div>
              </div>

              {/* Character Feature Spotlight Badge */}
              <div className={styles.characterBadge}>
                <span className={styles.characterIconBadge}>{item.characterIcon}</span>
                <span className={styles.characterNameText}>{item.characterTitle}</span>
              </div>

              {/* Card Main Body */}
              <div className={styles.cardContent}>
                <div className={styles.cardAccentLine} />
                <span className={styles.tagBadge}>{item.tagline}</span>
                <h2 className={styles.cardTitle}>{item.label}</h2>
                <p className={styles.cardDesc}>{item.description}</p>

                {/* Footer specs & Action Button */}
                <div className={styles.cardFooterBar}>
                  <span className={styles.difficultyPill}>
                    {item.difficultyBadge}
                  </span>

                  <button className={styles.cardBtn} tabIndex={-1}>
                    <span>{item.id === 'movies' ? 'PLAY MYSTERY' : 'TAKE EXAM'}</span>
                    <ArrowRight size={14} className={styles.cardBtnArrow} />
                  </button>
                </div>
              </div>

              {/* Active Selection Indicator */}
              {(isSelected || isHovered) && (
                <div className={styles.activeSelectionTag}>
                  <span className={styles.activeDot} />
                  <span>PREVIEWING THEME</span>
                </div>
              )}
            </motion.article>
          );
        })}
      </motion.main>

      {/* Footer */}
      <footer className={styles.footer}>
        <div className={styles.footerInner}>
          <img
            src="/assets/logos/Hunter Logo.svg"
            alt="Hunter Logo"
            className={styles.footerLogoHunter}
          />
          <div className={styles.footerDivider} />
          <img
            src="/assets/logos/Open Minds Logo.svg"
            alt="OMC Logo"
            className={styles.footerLogoOmc}
          />
          <span className={styles.footerText}>
            HUNTER × HUNTER | OPEN MINDS CLUB — ENTER THE EXAM. PROVE YOUR KNOWLEDGE.
          </span>
        </div>
      </footer>
    </div>
  );
}
