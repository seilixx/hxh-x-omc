# WHO AM I? — THE ANIME HUNTER EXAM
## Open Minds Club × Hunter × Hunter

An interactive anime character guessing game where the **machine** challenges the player to identify characters from four anime universes within a 2-minute time limit.

---

## 🎮 Game Concept

- The machine randomly selects a character and shows a **blurred image**
- A 2-minute countdown begins
- Every **30 seconds**, a hint is revealed and the image gets clearer
- The player types character names to guess — case-insensitive, typo-tolerant
- **Faster correct answers earn more points**

### Scoring
| Time of Correct Answer | Points |
|---|---|
| 0:00 – 0:29 | 100 |
| 0:30 – 0:59 | 80 |
| 1:00 – 1:29 | 60 |
| 1:30 – 1:59 | 40 |
| Timeout | 0 |

---

## 🌌 Anime Universes

1. **Hunter × Hunter** *(Main — 50+ characters)*
2. **Naruto** *(20+ characters)*
3. **Jujutsu Kaisen** *(15+ characters)*
4. **One Piece** *(20+ characters)*

---

## 🚀 Installation & Launch

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Then open **http://localhost:5173** in your browser.

---

## 📁 Project Structure

```
src/
├── components/
│   ├── LoadingScreen/     # Cinematic intro animation
│   ├── ConfigScreen/      # Game setup (mode, difficulty, rounds)
│   ├── GameScreen/        # Core gameplay (blur, timer, hints, answer)
│   ├── ResultScreen/      # Post-round character reveal & stats
│   └── SessionSummary/    # End-of-session score breakdown
├── data/
│   ├── hunter-x-hunter/characters.ts
│   ├── naruto/characters.ts
│   ├── jujutsu-kaisen/characters.ts
│   └── one-piece/characters.ts
├── hooks/
│   ├── useGameTimer.ts        # High-precision rAF timer
│   └── useCharacterSelection.ts
├── pages/
│   ├── HomePage.tsx           # Universe selection
│   ├── GamePage.tsx           # Game orchestrator
│   └── LeaderboardPage.tsx    # Local leaderboard
├── services/
│   ├── answerValidator.ts     # Fuzzy answer matching
│   ├── characterService.ts    # Character filtering & selection
│   └── storageService.ts      # LocalStorage persistence
├── styles/
│   └── global.css             # Design system & CSS variables
└── types/index.ts             # TypeScript interfaces
```

---

## 🖼 Adding Character Images

Place your own character images in:
```
public/assets/characters/<anime-name>/<character-name>.png
```

Then update the `image` field in the character data files to:
```
/assets/characters/hunter-x-hunter/gon.png
```

---

## 🏷 Adding the OMC Logo

Place your logo at:
```
public/assets/logos/omc-logo.png
```

Then replace the text `OMC` placeholders in the `LoadingScreen` and `Nav` components with an `<img>` tag.

---

## 🛠 Tech Stack

- **React 19** + **TypeScript**
- **Vite** (build tool)
- **Framer Motion** (animations)
- **React Router DOM** (navigation)
- **Lucide React** (icons)
- **CSS Modules** (scoped styles)
- **LocalStorage** (leaderboard persistence)

---

*OPEN MINDS CLUB — ENTER THE EXAM. PROVE YOUR KNOWLEDGE.*
