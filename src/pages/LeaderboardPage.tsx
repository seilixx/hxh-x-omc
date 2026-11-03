import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ArrowLeft,
  Trophy,
  Crown,
  Medal,
  Clock,
  Search,
  RotateCcw,
  Play,
  Award,
  Sparkles,
  Zap,
  Trash2,
} from 'lucide-react';
import {
  getLeaderboard,
  clearLeaderboard,
  resetLeaderboard,
  getPrefs,
} from '../services/storageService';
import type { LeaderboardCategory, GameMode } from '../types';
import { SpiderWebBackground } from '../components/common/SpiderWebBackground';
import { HxhOmcBrandHeader } from '../components/brand/HxhOmcBrandHeader';
import styles from './LeaderboardPage.module.css';

type CategoryFilter = 'all' | LeaderboardCategory;
type ModeFilter = 'all' | GameMode;
type SortOption = 'score' | 'accuracy' | 'speed' | 'date';

const CATEGORIES: { id: CategoryFilter; label: string; accent: string }[] = [
  { id: 'all', label: 'ALL CHALLENGES', accent: '#4ADE80' },
  { id: 'hunter-x-hunter', label: 'HUNTER × HUNTER', accent: '#4ADE80' },
  { id: 'naruto', label: 'NARUTO', accent: '#F97316' },
  { id: 'jujutsu-kaisen', label: 'JUJUTSU KAISEN', accent: '#A855F7' },
  { id: 'one-piece', label: 'ONE PIECE', accent: '#EAB308' },
  { id: 'marvel', label: 'MARVEL UNIVERSE', accent: '#EF4444' },
  { id: 'football', label: 'WORLD FOOTBALL', accent: '#10B981' },
  { id: 'movies', label: 'GUESS THE MOVIE', accent: '#F43F5E' },
];

const CATEGORY_META: Record<string, { label: string; accent: string }> = {
  'hunter-x-hunter': { label: 'Hunter × Hunter', accent: '#4ADE80' },
  naruto: { label: 'Naruto', accent: '#F97316' },
  'jujutsu-kaisen': { label: 'Jujutsu Kaisen', accent: '#A855F7' },
  'one-piece': { label: 'One Piece', accent: '#EAB308' },
  marvel: { label: 'Marvel Universe', accent: '#EF4444' },
  football: { label: 'World Football', accent: '#10B981' },
  movies: { label: 'Cinema Mystery', accent: '#F43F5E' },
};

export default function LeaderboardPage() {
  const navigate = useNavigate();
  const prefs = getPrefs();
  const currentCandidate = prefs.nickname && prefs.nickname !== 'Hunter' ? prefs.nickname : null;

  const [board, setBoard] = useState(getLeaderboard());
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>('all');
  const [modeFilter, setModeFilter] = useState<ModeFilter>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<SortOption>('score');

  // Filter and sort entries
  const processedEntries = useMemo(() => {
    let result = [...board];

    // Category filter
    if (categoryFilter !== 'all') {
      result = result.filter(e => e.anime === categoryFilter);
    }

    // Mode filter
    if (modeFilter !== 'all') {
      result = result.filter(e => e.mode === modeFilter);
    }

    // Search query
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(e => e.nickname.toLowerCase().includes(q));
    }

    // Sort
    result.sort((a, b) => {
      if (sortBy === 'score') return b.totalScore - a.totalScore;
      if (sortBy === 'accuracy') {
        const accA = a.totalRounds > 0 ? a.correctGuesses / a.totalRounds : 0;
        const accB = b.totalRounds > 0 ? b.correctGuesses / b.totalRounds : 0;
        return accB - accA;
      }
      if (sortBy === 'speed') {
        const timeA = a.bestTime > 0 ? a.bestTime : 999;
        const timeB = b.bestTime > 0 ? b.bestTime : 999;
        return timeA - timeB;
      }
      if (sortBy === 'date') {
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      }
      return 0;
    });

    return result;
  }, [board, categoryFilter, modeFilter, searchQuery, sortBy]);

  // Top 3 Podium
  const top1 = processedEntries[0];
  const top2 = processedEntries[1];
  const top3 = processedEntries[2];

  // Current candidate best
  const candidateBest = useMemo(() => {
    if (!currentCandidate) return null;
    const userEntries = board.filter(
      e => e.nickname.toLowerCase() === currentCandidate.toLowerCase()
    );
    if (userEntries.length === 0) return null;
    return userEntries.sort((a, b) => b.totalScore - a.totalScore)[0];
  }, [board, currentCandidate]);

  // Reset to default hall of fame
  const handleResetToDefault = () => {
    if (confirm('Reset to standard Hunter Association Hall of Fame records?')) {
      resetLeaderboard();
      setBoard(getLeaderboard());
    }
  };

  // Clear all
  const handleClearAll = () => {
    if (confirm('Clear all examination records from localStorage?')) {
      clearLeaderboard();
      setBoard([]);
    }
  };

  return (
    <div className={styles.page}>
      {/* Dynamic Universe Wallpaper reactive to Leaderboard Filter */}
      <SpiderWebBackground universe={categoryFilter === 'all' ? 'hunter-x-hunter' : categoryFilter} />

      {/* Top Header */}
      <header className={styles.header}>
        <button className={styles.backBtn} onClick={() => navigate('/')}>
          <ArrowLeft size={16} /> RETURN TO MAIN HUB
        </button>

        <div className={styles.headerCenter}>
          <div className={styles.headerBadge}>
            <Trophy size={12} />
            <span>EXAMINATION ARCHIVES • HALL OF FAME</span>
          </div>
          <h1 className={styles.title}>GLOBAL HUNTER LEADERBOARD</h1>
        </div>

        <div className={styles.headerActions}>
          <button className={styles.playCtaBtn} onClick={() => navigate('/')}>
            <Play size={14} /> PLAY EXAM
          </button>
          <button className={styles.resetBtn} onClick={handleResetToDefault} title="Restore Hall of Fame baseline">
            <RotateCcw size={13} /> RESTORE
          </button>
          <button className={styles.resetBtn} onClick={handleClearAll} title="Clear all local examination records">
            <Trash2 size={13} /> CLEAR
          </button>
        </div>
      </header>

      {/* Brand Header */}
      <div style={{ display: 'flex', justifyContent: 'center', padding: '16px 20px 0', position: 'relative', zIndex: 2 }}>
        <HxhOmcBrandHeader
          size="compact"
          subtitle="OFFICIAL HUNTER ASSOCIATION REGISTRY • POWERED BY OPEN MINDS CLUB"
          showSubtitle={true}
        />
      </div>

      <main className={styles.container}>
        {/* Active Candidate Banner */}
        {currentCandidate && (
          <div className={styles.registeredBanner}>
            <div className={styles.candidateLeft}>
              <div className={styles.candidateAvatar}>
                {currentCandidate.charAt(0).toUpperCase()}
              </div>
              <div>
                <div className={styles.candidateInfoTitle}>
                  REGISTERED EXAMINEE: {currentCandidate.toUpperCase()} (TAG #404)
                </div>
                <div className={styles.candidateSub}>
                  {candidateBest
                    ? `Personal Best: ${candidateBest.totalScore} PTS • ${candidateBest.correctGuesses}/${candidateBest.totalRounds} Correct (${candidateBest.mode})`
                    : 'No exam scores recorded yet for your tag. Take an exam to enter the rankings!'}
                </div>
              </div>
            </div>
            <button className={styles.playCtaBtn} onClick={() => navigate('/')}>
              <Zap size={14} /> NEW TRIAL
            </button>
          </div>
        )}

        {/* TOP 3 PODIUM HERO */}
        {processedEntries.length >= 3 && !searchQuery && (
          <div className={styles.podiumSection}>
            {/* 2nd Place */}
            {top2 && (
              <motion.div
                className={`${styles.podiumCard} ${styles.podiumSecond}`}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
              >
                <div className={`${styles.podiumRankBadge} ${styles.rankBadgeSecond}`}>
                  <Medal size={14} style={{ display: 'inline', marginRight: '4px' }} /> #2 SILVER
                </div>
                <div className={styles.podiumName}>{top2.nickname}</div>
                <div className={styles.podiumScore}>{top2.totalScore} PTS</div>
                <div
                  className={styles.podiumCategory}
                  style={{ color: CATEGORY_META[top2.anime]?.accent || '#FFF' }}
                >
                  {CATEGORY_META[top2.anime]?.label || top2.anime}
                </div>
                <div style={{ fontSize: '11px', color: '#94A3B8', marginTop: '6px' }}>
                  Best: {top2.bestTime}s • {top2.correctGuesses}/{top2.totalRounds}
                </div>
              </motion.div>
            )}

            {/* 1st Place Champion */}
            {top1 && (
              <motion.div
                className={`${styles.podiumCard} ${styles.podiumFirst}`}
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                <Crown size={28} className={styles.podiumCrown} />
                <div className={`${styles.podiumRankBadge} ${styles.rankBadgeFirst}`}>
                  👑 #1 GRANDMASTER
                </div>
                <div className={styles.podiumName} style={{ fontSize: '19px' }}>{top1.nickname}</div>
                <div className={styles.podiumScore} style={{ fontSize: '32px' }}>{top1.totalScore} PTS</div>
                <div
                  className={styles.podiumCategory}
                  style={{
                    color: CATEGORY_META[top1.anime]?.accent || '#FFF',
                    background: 'rgba(250, 204, 21, 0.15)',
                    border: '1px solid rgba(250, 204, 21, 0.3)',
                  }}
                >
                  {CATEGORY_META[top1.anime]?.label || top1.anime}
                </div>
                <div style={{ fontSize: '12px', color: '#FDE047', fontWeight: 'bold', marginTop: '6px' }}>
                  ⚡ Record Speed: {top1.bestTime}s • Perfect {top1.correctGuesses}/{top1.totalRounds}
                </div>
              </motion.div>
            )}

            {/* 3rd Place */}
            {top3 && (
              <motion.div
                className={`${styles.podiumCard} ${styles.podiumThird}`}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                <div className={`${styles.podiumRankBadge} ${styles.rankBadgeThird}`}>
                  <Medal size={14} style={{ display: 'inline', marginRight: '4px' }} /> #3 BRONZE
                </div>
                <div className={styles.podiumName}>{top3.nickname}</div>
                <div className={styles.podiumScore}>{top3.totalScore} PTS</div>
                <div
                  className={styles.podiumCategory}
                  style={{ color: CATEGORY_META[top3.anime]?.accent || '#FFF' }}
                >
                  {CATEGORY_META[top3.anime]?.label || top3.anime}
                </div>
                <div style={{ fontSize: '11px', color: '#94A3B8', marginTop: '6px' }}>
                  Best: {top3.bestTime}s • {top3.correctGuesses}/{top3.totalRounds}
                </div>
              </motion.div>
            )}
          </div>
        )}

        {/* CONTROLS TOOLBAR */}
        <div className={styles.toolbar}>
          {/* Search and Sort Row */}
          <div className={styles.searchSortRow}>
            <div className={styles.searchWrap}>
              <Search size={16} className={styles.searchIcon} />
              <input
                type="text"
                className={styles.searchInput}
                placeholder="Search candidates by name (e.g. Killua, Gojo, Messi)..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
              />
              {searchQuery && (
                <button className={styles.clearSearchBtn} onClick={() => setSearchQuery('')}>
                  CLEAR
                </button>
              )}
            </div>

            <div className={styles.sortWrap}>
              <span className={styles.sortLabel}>SORT BY:</span>
              <select
                className={styles.sortSelect}
                value={sortBy}
                onChange={e => setSortBy(e.target.value as SortOption)}
              >
                <option value="score">Highest Score</option>
                <option value="accuracy">Best Accuracy</option>
                <option value="speed">Fastest Speed</option>
                <option value="date">Most Recent</option>
              </select>
            </div>
          </div>

          {/* Category Filter Pills */}
          <div className={styles.categoryPills}>
            {CATEGORIES.map(cat => {
              const active = categoryFilter === cat.id;
              return (
                <button
                  key={cat.id}
                  className={`${styles.categoryPill} ${active ? styles.categoryPillActive : ''}`}
                  style={{ '--pill-accent': cat.accent } as React.CSSProperties}
                  onClick={() => setCategoryFilter(cat.id)}
                >
                  {cat.label}
                </button>
              );
            })}
          </div>

          {/* Game Mode Filter Pills */}
          <div className={styles.modePills}>
            <span className={styles.modeLabel}>MODE:</span>
            {[
              { id: 'all' as ModeFilter, label: 'ALL MODES' },
              { id: 'classic' as ModeFilter, label: 'CLASSIC' },
              { id: 'time-attack' as ModeFilter, label: 'TIME ATTACK' },
              { id: 'endless' as ModeFilter, label: 'ENDLESS' },
            ].map(m => (
              <button
                key={m.id}
                className={`${styles.modeBtn} ${modeFilter === m.id ? styles.modeBtnActive : ''}`}
                onClick={() => setModeFilter(m.id)}
              >
                {m.label}
              </button>
            ))}
            <span style={{ marginLeft: 'auto', fontSize: '11px', color: '#94A3B8' }}>
              Showing {processedEntries.length} Records
            </span>
          </div>
        </div>

        {/* LEADERBOARD TABLE */}
        <div className={styles.tableContainer}>
          {processedEntries.length === 0 ? (
            <div className={styles.emptyState}>
              <Award size={48} color="#64748B" />
              <div className={styles.emptyTitle}>NO MATCHING RECORDS FOUND</div>
              <p style={{ maxWidth: '420px', margin: '0 auto 16px', fontSize: '13px' }}>
                {searchQuery
                  ? `No examinee matched "${searchQuery}". Clear your search or change category filters.`
                  : 'No entries registered under this category yet.'}
              </p>
              <button className={styles.playCtaBtn} onClick={handleResetToDefault}>
                <RotateCcw size={14} /> RESTORE HALL OF FAME
              </button>
            </div>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>RANK</th>
                  <th>EXAMINEE</th>
                  <th>CATEGORY</th>
                  <th>MODE</th>
                  <th>SCORE</th>
                  <th>ACCURACY</th>
                  <th>SPEED</th>
                  <th>DATE</th>
                </tr>
              </thead>
              <tbody>
                {processedEntries.map((entry, idx) => {
                  const meta = CATEGORY_META[entry.anime] || {
                    label: entry.anime,
                    accent: '#4ADE80',
                  };
                  const isCurrentCandidate =
                    currentCandidate &&
                    entry.nickname.toLowerCase() === currentCandidate.toLowerCase();
                  const acc =
                    entry.totalRounds > 0
                      ? Math.round((entry.correctGuesses / entry.totalRounds) * 100)
                      : 100;
                  const dateStr = entry.date
                    ? new Date(entry.date).toLocaleDateString(undefined, {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                      })
                    : 'Recent';

                  const rankDisplay =
                    idx === 0
                      ? '👑 #1'
                      : idx === 1
                      ? '🥈 #2'
                      : idx === 2
                      ? '🥉 #3'
                      : `#${idx + 1}`;

                  return (
                    <motion.tr
                      key={entry.id}
                      className={`${styles.tableRow} ${
                        isCurrentCandidate ? styles.tableRowHighlight : ''
                      }`}
                      initial={{ opacity: 0, y: 6 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: Math.min(idx * 0.02, 0.3) }}
                    >
                      {/* Rank */}
                      <td
                        className={styles.rankCell}
                        style={{
                          color:
                            idx === 0
                              ? '#FACC15'
                              : idx === 1
                              ? '#CBD5E1'
                              : idx === 2
                              ? '#FB923C'
                              : '#64748B',
                        }}
                      >
                        {rankDisplay}
                      </td>

                      {/* Examinee */}
                      <td>
                        <div className={styles.playerCell}>
                          <div
                            className={styles.playerAvatar}
                            style={{
                              borderColor: meta.accent,
                              boxShadow: idx < 3 ? `0 0 8px ${meta.accent}60` : 'none',
                            }}
                          >
                            {entry.nickname.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <span className={styles.playerName}>{entry.nickname}</span>
                            {isCurrentCandidate && (
                              <span className={styles.youBadge}>YOU</span>
                            )}
                          </div>
                        </div>
                      </td>

                      {/* Category */}
                      <td>
                        <span
                          className={styles.categoryBadge}
                          style={{
                            color: meta.accent,
                            borderColor: `${meta.accent}45`,
                            background: `${meta.accent}14`,
                          }}
                        >
                          <Sparkles size={11} />
                          {meta.label}
                        </span>
                      </td>

                      {/* Mode */}
                      <td>
                        <span className={styles.modeBadge}>{entry.mode}</span>
                      </td>

                      {/* Score */}
                      <td>
                        <span className={styles.scoreCell} style={{ color: meta.accent }}>
                          {entry.totalScore} PTS
                        </span>
                      </td>

                      {/* Accuracy */}
                      <td>
                        <div className={styles.accuracyCell}>
                          <div className={styles.accBarBg}>
                            <div
                              className={styles.accBarFill}
                              style={{ width: `${acc}%`, background: meta.accent }}
                            />
                          </div>
                          <span className={styles.accText}>
                            {acc}% ({entry.correctGuesses}/{entry.totalRounds})
                          </span>
                        </div>
                      </td>

                      {/* Best Speed */}
                      <td>
                        <span className={styles.timeCell}>
                          <Clock size={12} style={{ display: 'inline', marginRight: '4px' }} />
                          {entry.bestTime > 0 ? `${entry.bestTime}s` : '--'}
                        </span>
                      </td>

                      {/* Date */}
                      <td className={styles.dateCell}>{dateStr}</td>
                    </motion.tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      </main>
    </div>
  );
}
