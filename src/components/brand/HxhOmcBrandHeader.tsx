import React from 'react';
import styles from './HxhOmcBrandHeader.module.css';

interface HxhOmcBrandHeaderProps {
  size?: 'normal' | 'large' | 'compact';
  subtitle?: string;
  showSubtitle?: boolean;
}

export const HxhOmcBrandHeader: React.FC<HxhOmcBrandHeaderProps> = ({
  size = 'normal',
  subtitle = 'THE ANIME HUNTER EXAM • OPEN MINDS CLUB',
  showSubtitle = true,
}) => {
  return (
    <div className={`${styles.brandContainer} ${styles[size]}`}>
      {/* Logos and Divider Lockup */}
      <div className={styles.logoRow}>
        {/* Hunter x Hunter Official Outline Logo */}
        <div className={styles.hunterLogoWrapper}>
          <img
            src="/assets/logos/Hunter Logo.svg"
            alt="Hunter x Hunter"
            className={styles.hunterLogo}
          />

          {/* Hanging Glowing Spiders Dangling from Hunter Logo */}
          <div className={styles.spidersContainer}>
            {/* Spider 1 (Left - hanging lower) */}
            <div className={`${styles.hangingSpider} ${styles.spiderLeft}`}>
              <div className={styles.silkThread} style={{ height: '85px' }} />
              <svg
                className={styles.spiderSvg}
                viewBox="0 0 60 70"
                width="34"
                height="40"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g filter="url(#glowLeft)">
                  {/* Abdomen / Body */}
                  <ellipse cx="30" cy="38" rx="8" ry="12" fill="#FFFFFF" />
                  {/* Head */}
                  <circle cx="30" cy="22" r="5.5" fill="#FFFFFF" />
                  {/* Left Legs */}
                  <path d="M 26 26 C 18 20 12 22 4 16" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 25 30 C 16 28 10 32 3 28" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 25 36 C 15 37 8 45 4 52" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 26 42 C 18 46 12 56 8 64" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  {/* Right Legs */}
                  <path d="M 34 26 C 42 20 48 22 56 16" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 35 30 C 44 28 50 32 57 28" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 35 36 C 45 37 52 45 56 52" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 34 42 C 42 46 48 56 52 64" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                </g>
                <defs>
                  <filter id="glowLeft" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="0" stdDeviation="2.5" floodColor="#ffffff" floodOpacity="0.8" />
                    <feDropShadow dx="0" dy="0" stdDeviation="6" floodColor="#42d392" floodOpacity="0.5" />
                  </filter>
                </defs>
              </svg>
            </div>

            {/* Spider 2 (Right - hanging higher) */}
            <div className={`${styles.hangingSpider} ${styles.spiderRight}`}>
              <div className={styles.silkThread} style={{ height: '48px' }} />
              <svg
                className={styles.spiderSvg}
                viewBox="0 0 60 70"
                width="28"
                height="33"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g filter="url(#glowRight)">
                  {/* Abdomen / Body */}
                  <ellipse cx="30" cy="38" rx="8" ry="12" fill="#FFFFFF" />
                  {/* Head */}
                  <circle cx="30" cy="22" r="5.5" fill="#FFFFFF" />
                  {/* Left Legs */}
                  <path d="M 26 26 C 18 20 12 22 4 16" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 25 30 C 16 28 10 32 3 28" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 25 36 C 15 37 8 45 4 52" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 26 42 C 18 46 12 56 8 64" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  {/* Right Legs */}
                  <path d="M 34 26 C 42 20 48 22 56 16" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 35 30 C 44 28 50 32 57 28" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 35 36 C 45 37 52 45 56 52" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                  <path d="M 34 42 C 42 46 48 56 52 64" stroke="#FFFFFF" strokeWidth="2" strokeLinecap="round" />
                </g>
                <defs>
                  <filter id="glowRight" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="0" stdDeviation="2.5" floodColor="#ffffff" floodOpacity="0.8" />
                    <feDropShadow dx="0" dy="0" stdDeviation="6" floodColor="#42d392" floodOpacity="0.5" />
                  </filter>
                </defs>
              </svg>
            </div>
          </div>
        </div>

        {/* Crisp Vertical White Divider */}
        <div className={styles.divider} aria-hidden="true" />

        {/* Open Minds Club Official Logo */}
        <div className={styles.omcLogoWrapper}>
          <img
            src="/assets/logos/Open Minds Logo.svg"
            alt="Open Minds Club"
            className={styles.omcLogo}
          />
        </div>
      </div>

      {/* Subtitle */}
      {showSubtitle && subtitle && (
        <div className={styles.subtitleBadge}>
          <span className={styles.badgeKatakana}>ハンター試験</span>
          <span className={styles.subtitleText}>{subtitle}</span>
          <span className={styles.badgeKatakana}>オープンマインズ</span>
        </div>
      )}
    </div>
  );
};
