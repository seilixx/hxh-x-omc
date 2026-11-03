import { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import LoadingScreen from './components/LoadingScreen/LoadingScreen';
import HomePage from './pages/HomePage';
import GamePage from './pages/GamePage';
import LeaderboardPage from './pages/LeaderboardPage';
import MovieGamePage from './pages/MovieGamePage';

export default function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Minimum loading screen time for cinematic effect
    const timer = setTimeout(() => setLoading(false), 4200);
    return () => clearTimeout(timer);
  }, []);

  return (
    <AnimatePresence mode="wait">
      {loading ? (
        <LoadingScreen key="loading" onComplete={() => setLoading(false)} />
      ) : (
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/game/:anime" element={<GamePage />} />
          <Route path="/movies" element={<MovieGamePage />} />
          <Route path="/game/movies" element={<MovieGamePage />} />
          <Route path="/leaderboard" element={<LeaderboardPage />} />
        </Routes>
      )}
    </AnimatePresence>
  );
}
