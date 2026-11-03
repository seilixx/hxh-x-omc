import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  ArrowLeft,
  Settings,
  Shuffle,
  Clock,
  Zap,
  Infinity as InfinityIcon,
  User,
  Check,
  AlertCircle,
  Award,
  Shield,
  Users,
  Layers,
} from 'lucide-react';
import type { AnimeUniverse, GameConfig, GameMode, Difficulty } from '../../types';
import { ANIME_META } from '../../types';
import { filterCharacters } from '../../services/characterService';
import { getPrefs, savePrefs } from '../../services/storageService';
import { SpiderWebBackground } from '../common/SpiderWebBackground';
import { HxhOmcBrandHeader } from '../brand/HxhOmcBrandHeader';
import styles from './ConfigScreen.module.css';

interface Props {
  anime: AnimeUniverse;
  initialConfig: GameConfig;
  onStart: (config: GameConfig) => void;
  onBack: () => void;
}

const MODES: { id: GameMode; label: string; desc: string; icon: React.ReactNode }[] = [
  {
    id: 'classic',
    label: 'CLASSIC (TIMED)',
    desc: '2:00 timer, progressive hints at 30s/60s/90s, high score calculation',
    icon: <Settings size={18} />,
  },
  {
    id: 'time-attack',
    label: 'TIME ATTACK',
    desc: 'Rapid identification against the clock, leaderboard speed ranking',
    icon: <Zap size={18} />,
  },
  {
    id: 'endless',
    label: 'ENDLESS TRIAL',
    desc: 'Continuous candidate identification until you choose to exit',
    icon: <InfinityIcon size={18} />,
  },
];

const DIFFICULTIES: { id: Difficulty; label: string; color: string; desc: string }[] = [
  { id: 'easy', label: 'EASY', color: '#4ADE80', desc: 'Main characters & famous icons' },
  { id: 'medium', label: 'MEDIUM', color: '#FACC15', desc: 'Key allies, rivals & arc bosses' },
  { id: 'hard', label: 'HARD', color: '#F97316', desc: 'Deep lore & secondary figures' },
  { id: 'expert', label: 'EXPERT', color: '#EF4444', desc: 'Obscure & high-tier trivia' },
];

// Universe filter options
const HXH_ARCS = [
  'Hunter Exam Arc',
  'Heavens Arena Arc',
  'Yorknew City Arc',
  'Greed Island Arc',
  'Chimera Ant Arc',
  '13th Hunter Chairman Election Arc',
  'Succession Contest Arc',
];

const HXH_AFFILIATIONS = [
  'Hunters Association',
  'Zoldyck Family',
  'Phantom Troupe',
  'Chimera Ants',
];

const HXH_NEN_TYPES = [
  'Enhancement',
  'Transmutation',
  'Conjuration',
  'Emission',
  'Manipulation',
  'Specialization',
];

const NARUTO_ARCS = [
  'Land of Waves Arc',
  'Chunin Exams Arc',
  'Konoha Crush Arc',
  'Search for Tsunade Arc',
  'Sasuke Recovery Mission',
  'Kazekage Rescue Mission',
  'Akatsuki Suppression Arc',
  'Tale of Jiraiya & Pain',
  'Five Kage Summit Arc',
  'Fourth Shinobi World War',
  'Boruto Next Generations',
];

const JJK_ARCS = [
  'Introduction & Fearsome Womb',
  'Vs. Mahito Arc',
  'Kyoto Goodwill Event Arc',
  'Death Painting Arc',
  'Gojo\'s Past Arc (Hidden Inventory)',
  'Shibuya Incident Arc',
  'Culling Game Arc',
  'Shinjuku Showdown Arc',
];

const OP_ARCS = [
  'East Blue Saga',
  'Alabasta Saga',
  'Sky Island Saga (Skypiea)',
  'Water 7 / Enies Lobby',
  'Thriller Bark Saga',
  'Summit War (Marineford)',
  'Fish-Man Island Saga',
  'Dressrosa Saga',
  'Whole Cake Island Saga',
  'Wano Country Saga',
  'Final Saga (Egghead Island)',
];

const MARVEL_ARCS = [
  'Phase 1: Assemble',
  'Phase 2: Age of Heroes',
  'Phase 3: Infinity Saga',
  'Phase 4 & 5: Multiverse Saga',
  'Street-Level & Defenders',
  'Cosmic & Asgardian',
  'X-Men & Mutants',
];

const FOOTBALL_ARCS = [
  'Golden Era (1950s-1980s)',
  '90s World Cup Legends',
  'Galácticos & 2000s Era',
  'Messi vs Ronaldo Era (2010s)',
  'Modern Prodigies (2020s)',
];

const FOOTBALL_AFFILIATIONS = [
  'Real Madrid',
  'Barcelona',
  'Manchester United',
  'Bayern Munich',
  'Juventus / Serie A',
  'Santos / Brazil',
  'Argentina',
];

const UNIVERSE_ARCS: Record<AnimeUniverse, { title: string; arcs: string[] }> = {
  'hunter-x-hunter': {
    title: 'STORY ARCS (HUNTER × HUNTER)',
    arcs: HXH_ARCS,
  },
  naruto: {
    title: 'CHRONOLOGY & ARCS (NARUTO)',
    arcs: NARUTO_ARCS,
  },
  'jujutsu-kaisen': {
    title: 'STORY ARCS (JUJUTSU KAISEN)',
    arcs: JJK_ARCS,
  },
  'one-piece': {
    title: 'SAGAS & ISLANDS (ONE PIECE)',
    arcs: OP_ARCS,
  },
  marvel: {
    title: 'CINEMATIC PHASES & REALMS (MARVEL)',
    arcs: MARVEL_ARCS,
  },
  football: {
    title: 'ERAS & GENERATIONS (WORLD FOOTBALL)',
    arcs: FOOTBALL_ARCS,
  },
};

export default function ConfigScreen({ anime, initialConfig, onStart, onBack }: Props) {
  const meta = ANIME_META[anime];
  const prefs = getPrefs();
  const [config, setConfig] = useState<GameConfig>(initialConfig);
  const [nickname, setNickname] = useState(
    prefs.nickname && prefs.nickname !== 'Hunter' ? prefs.nickname : ''
  );
  const [nameError, setNameError] = useState<string | null>(null);

  const handleNicknameChange = (val: string) => {
    setNickname(val);
    if (val.trim()) {
      setNameError(null);
      savePrefs({ nickname: val.trim() });
    }
  };

  const toggleDifficulty = (d: Difficulty) => {
    setConfig(prev => {
      const has = prev.difficulty.includes(d);
      if (has && prev.difficulty.length === 1) return prev; // keep at least 1
      return {
        ...prev,
        difficulty: has ? prev.difficulty.filter(x => x !== d) : [...prev.difficulty, d],
      };
    });
  };

  const toggleArrayFilter = (field: keyof GameConfig, item: string) => {
    setConfig(prev => {
      const current = (prev[field] as string[]) || [];
      const has = current.includes(item);
      const updated = has ? current.filter(x => x !== item) : [...current, item];
      return {
        ...prev,
        [field]: updated.length > 0 ? updated : undefined,
      };
    });
  };

  const handleBeginExam = () => {
    const cleanName = nickname.trim();
    if (!cleanName || cleanName.toLowerCase() === 'hunter') {
      setNameError('Please enter your Examinee Candidate Name before beginning.');
      return;
    }

    const currentMatching = filterCharacters(config);
    if (currentMatching.length === 0) {
      alert('No candidates match your current filters. Please select more difficulties or story arcs.');
      return;
    }

    setNameError(null);
    savePrefs({
      nickname: cleanName,
      lastMode: config.mode,
      lastDifficulty: config.difficulty,
      lastAnime: anime,
    });
    onStart(config);
  };

  // Preview matching characters count
  const matchingPool = filterCharacters(config);

  return (
    <motion.div
      className={styles.page}
      style={{ '--accent': meta.accent, '--glow': meta.glow } as React.CSSProperties}
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      {/* Dynamic Universe Character Background */}
      <SpiderWebBackground universe={anime} />

      {/* Header */}
      <header className={styles.header}>
        <button className={styles.backBtn} onClick={onBack}>
          <ArrowLeft size={16} /> BACK TO MAIN HUB
        </button>

        <div className={styles.headerCenter}>
          <div className={styles.examMarqueeBadge}>
            <Shield size={12} />
            <span>OPEN MINDS CLUB • {meta.examLabel.toUpperCase()}</span>
          </div>
          <h1 className={styles.headerTitle}>{meta.label} EXAMINATION</h1>
        </div>

        <div className={styles.headerRight}>
          <div className={styles.poolBadge}>
            <Users size={14} />
            <span>{matchingPool.length} CANDIDATES READY</span>
          </div>
        </div>
      </header>

      {/* Main Configuration Card */}
      <main className={styles.container}>
        {/* Brand Header Banner */}
        <div className={styles.brandBanner}>
          <HxhOmcBrandHeader
            size="compact"
            subtitle={`EXAMINATION BOARD • ${meta.label.toUpperCase()} REGISTRATION`}
            showSubtitle={true}
          />
        </div>

        <motion.div
          className={styles.configCard}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          {/* ── 1. Examinee Candidate Registration ── */}
          <div className={styles.sectionCard}>
            <div className={styles.sectionHeaderRow}>
              <label className={styles.sectionTitle}>
                <User size={16} className={styles.sectionIcon} />
                <span>EXAMINEE CANDIDATE NAME</span>
                <span className={styles.mandatoryBadge}>(REQUIRED)</span>
              </label>
              <span className={styles.tagNumberBadge}>TAG #404</span>
            </div>
            <p className={styles.sectionDesc}>
              Enter your official Examinee name or alias. Your examination score and rating will be recorded directly on the global leaderboard.
            </p>
            <div className={styles.inputWrapper}>
              <User size={18} className={styles.inputIcon} />
              <input
                type="text"
                className={`${styles.textInput} ${nameError ? styles.inputError : ''}`}
                value={nickname}
                onChange={e => handleNicknameChange(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleBeginExam()}
                placeholder="Enter your candidate name / Hunter alias..."
                maxLength={24}
              />
            </div>
            {nameError && (
              <div className={styles.errorText}>
                <AlertCircle size={14} /> {nameError}
              </div>
            )}
          </div>

          {/* ── 2. Game Mode Selection ── */}
          <div className={styles.sectionCard}>
            <div className={styles.sectionHeaderRow}>
              <label className={styles.sectionTitle}>
                <Settings size={16} className={styles.sectionIcon} />
                <span>EXAMINATION MODE</span>
              </label>
              <span className={styles.activePillBadge}>{config.mode.toUpperCase()}</span>
            </div>
            <div className={styles.modeGrid}>
              {MODES.map(m => {
                const isActive = config.mode === m.id;
                return (
                  <button
                    key={m.id}
                    type="button"
                    className={`${styles.modeBtn} ${isActive ? styles.modeBtnActive : ''}`}
                    onClick={() => setConfig(p => ({ ...p, mode: m.id }))}
                  >
                    <div className={styles.modeBtnTop}>
                      <span className={styles.modeBtnIcon}>{m.icon}</span>
                      <span className={styles.modeBtnLabel}>{m.label}</span>
                      {isActive && <Check size={14} className={styles.modeCheck} />}
                    </div>
                    <p className={styles.modeBtnDesc}>{m.desc}</p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* ── 3. Difficulty Tiers (Multi-select) ── */}
          <div className={styles.sectionCard}>
            <div className={styles.sectionHeaderRow}>
              <label className={styles.sectionTitle}>
                <Award size={16} className={styles.sectionIcon} />
                <span>DIFFICULTY TIERS</span>
                <span className={styles.multiTag}>MULTI-SELECT</span>
              </label>
              <div className={styles.filterActions}>
                <button
                  type="button"
                  className={styles.filterActionBtn}
                  onClick={() =>
                    setConfig(prev => ({ ...prev, difficulty: ['easy', 'medium', 'hard', 'expert'] }))
                  }
                >
                  SELECT ALL
                </button>
                <button
                  type="button"
                  className={styles.filterActionBtn}
                  onClick={() => setConfig(prev => ({ ...prev, difficulty: ['easy'] }))}
                >
                  EASY ONLY
                </button>
              </div>
            </div>
            <div className={styles.diffGrid}>
              {DIFFICULTIES.map(d => {
                const active = config.difficulty.includes(d.id);
                return (
                  <button
                    key={d.id}
                    type="button"
                    className={`${styles.diffBtn} ${active ? styles.diffBtnActive : ''}`}
                    style={{ '--diff-color': d.color } as React.CSSProperties}
                    onClick={() => toggleDifficulty(d.id)}
                  >
                    <div className={styles.diffBtnTop}>
                      <span className={styles.diffDot} />
                      <span className={styles.diffLabel}>{d.label}</span>
                      {active && <Check size={14} className={styles.diffCheck} />}
                    </div>
                    <span className={styles.diffDesc}>{d.desc}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* ── 4. Examination Length / Rounds ── */}
          <div className={styles.sectionCard}>
            <div className={styles.sectionHeaderRow}>
              <label className={styles.sectionTitle}>
                <Clock size={16} className={styles.sectionIcon} />
                <span>EXAMINATION LENGTH (ROUNDS)</span>
              </label>
              <span className={styles.activePillBadge}>
                {config.mode === 'endless' ? 'ENDLESS' : `${config.rounds} ROUNDS`}
              </span>
            </div>
            <div className={styles.roundsGrid}>
              {[5, 10, 15, 20].map(r => {
                const isActive = config.rounds === r && config.mode !== 'endless';
                return (
                  <button
                    key={r}
                    type="button"
                    disabled={config.mode === 'endless'}
                    className={`${styles.roundBtn} ${isActive ? styles.roundBtnActive : ''}`}
                    onClick={() => setConfig(p => ({ ...p, rounds: r }))}
                  >
                    {isActive && <Check size={13} />}
                    <span>{r} CANDIDATES</span>
                  </button>
                );
              })}
              <button
                type="button"
                className={`${styles.roundBtn} ${config.mode === 'endless' ? styles.roundBtnActive : ''}`}
                onClick={() => setConfig(p => ({ ...p, mode: 'endless' }))}
              >
                {config.mode === 'endless' && <Check size={13} />}
                <span>FULL / ENDLESS POOL</span>
              </button>
            </div>
          </div>

          {/* ── 5. Story Arcs / Chronology Filter ── */}
          {UNIVERSE_ARCS[anime] && (
            <div className={styles.sectionCard}>
              <div className={styles.sectionHeaderRow}>
                <label className={styles.sectionTitle}>
                  <Layers size={16} className={styles.sectionIcon} />
                  <span>{UNIVERSE_ARCS[anime].title}</span>
                </label>
                <div className={styles.filterActions}>
                  <button
                    type="button"
                    className={styles.filterActionBtn}
                    onClick={() =>
                      setConfig(prev => ({ ...prev, arc: [...UNIVERSE_ARCS[anime].arcs] }))
                    }
                  >
                    SELECT ALL
                  </button>
                  <button
                    type="button"
                    className={styles.filterActionBtn}
                    onClick={() => setConfig(prev => ({ ...prev, arc: undefined }))}
                  >
                    CLEAR ALL
                  </button>
                </div>
              </div>
              <div className={styles.chipGrid}>
                {UNIVERSE_ARCS[anime].arcs.map(arc => {
                  const active = (config.arc || []).includes(arc);
                  return (
                    <button
                      key={arc}
                      type="button"
                      className={`${styles.chip} ${active ? styles.chipActive : ''}`}
                      onClick={() => toggleArrayFilter('arc', arc)}
                    >
                      {active && <Check size={12} />}
                      <span>{arc}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* ── 6. Secondary Universe-Specific Filters ── */}
          {anime === 'hunter-x-hunter' && (
            <>
              <div className={styles.sectionCard}>
                <label className={styles.sectionTitle}>
                  <Shield size={16} className={styles.sectionIcon} />
                  <span>NEN CLASSIFICATION</span>
                </label>
                <div className={styles.chipGrid}>
                  {HXH_NEN_TYPES.map(nen => {
                    const active = (config.hxhNenType || []).includes(nen);
                    return (
                      <button
                        key={nen}
                        type="button"
                        className={`${styles.chip} ${active ? styles.chipActive : ''}`}
                        onClick={() => toggleArrayFilter('hxhNenType', nen)}
                      >
                        {active && <Check size={12} />}
                        <span>{nen}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className={styles.sectionCard}>
                <label className={styles.sectionTitle}>
                  <Shield size={16} className={styles.sectionIcon} />
                  <span>AFFILIATIONS & FACTIONS</span>
                </label>
                <div className={styles.chipGrid}>
                  {HXH_AFFILIATIONS.map(aff => {
                    const active = (config.hxhAffiliation || []).includes(aff);
                    return (
                      <button
                        key={aff}
                        type="button"
                        className={`${styles.chip} ${active ? styles.chipActive : ''}`}
                        onClick={() => toggleArrayFilter('hxhAffiliation', aff)}
                      >
                        {active && <Check size={12} />}
                        <span>{aff}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            </>
          )}

          {anime === 'football' && (
            <div className={styles.sectionCard}>
              <label className={styles.sectionTitle}>
                <Shield size={16} className={styles.sectionIcon} />
                <span>FOOTBALL CLUBS & NATIONS</span>
              </label>
              <div className={styles.chipGrid}>
                {FOOTBALL_AFFILIATIONS.map(aff => {
                  const active = (config.footballAffiliation || []).includes(aff);
                  return (
                    <button
                      key={aff}
                      type="button"
                      className={`${styles.chip} ${active ? styles.chipActive : ''}`}
                      onClick={() => toggleArrayFilter('footballAffiliation', aff)}
                    >
                      {active && <Check size={12} />}
                      <span>{aff}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* ── 7. Grand Examination Start Action Button ── */}
          <div className={styles.startSection}>
            <motion.button
              type="button"
              className={styles.commenceBtn}
              onClick={handleBeginExam}
              disabled={matchingPool.length === 0}
              whileHover={{ scale: matchingPool.length > 0 ? 1.015 : 1 }}
              whileTap={{ scale: matchingPool.length > 0 ? 0.985 : 1 }}
            >
              <Shuffle size={20} />
              <span>
                {matchingPool.length === 0
                  ? 'NO CANDIDATES MATCH CURRENT FILTERS'
                  : `COMMENCE ${meta.label.toUpperCase()} EXAMINATION (${matchingPool.length} CANDIDATES) →`}
              </span>
            </motion.button>

            <p className={styles.examNotice}>
              <Clock size={14} />
              <span>Official 2:00 duration per round • Progressive hints at 0:30, 1:00, and 1:30</span>
            </p>
          </div>
        </motion.div>
      </main>
    </motion.div>
  );
}
