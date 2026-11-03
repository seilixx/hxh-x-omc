import { useState, useEffect, useRef, useCallback } from 'react';
import { ROUND_DURATION } from '../types';

interface UseGameTimerReturn {
  elapsedTime: number;
  isRunning: boolean;
  start: () => void;
  stop: () => void;
  reset: () => void;
}

export function useGameTimer(onTick?: (elapsed: number) => void, onExpire?: () => void): UseGameTimerReturn {
  const [elapsedTime, setElapsedTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const startTimeRef = useRef<number | null>(null);
  const pausedElapsedRef = useRef(0);
  const animFrameRef = useRef<number | null>(null);
  const expiredRef = useRef(false);

  const tick = useCallback(() => {
    if (startTimeRef.current === null) return;
    const now = performance.now();
    const elapsed = Math.floor((now - startTimeRef.current) / 1000) + pausedElapsedRef.current;
    const clamped = Math.min(elapsed, ROUND_DURATION);

    setElapsedTime(clamped);
    onTick?.(clamped);

    if (clamped >= ROUND_DURATION) {
      if (!expiredRef.current) {
        expiredRef.current = true;
        setIsRunning(false);
        onExpire?.();
      }
      return;
    }

    animFrameRef.current = requestAnimationFrame(tick);
  }, [onTick, onExpire]);

  const start = useCallback(() => {
    expiredRef.current = false;
    startTimeRef.current = performance.now();
    setIsRunning(true);
    animFrameRef.current = requestAnimationFrame(tick);
  }, [tick]);

  const stop = useCallback(() => {
    setIsRunning(false);
    if (animFrameRef.current) {
      cancelAnimationFrame(animFrameRef.current);
      animFrameRef.current = null;
    }
    // Save elapsed so far
    if (startTimeRef.current !== null) {
      pausedElapsedRef.current = Math.min(
        Math.floor((performance.now() - startTimeRef.current) / 1000) + pausedElapsedRef.current,
        ROUND_DURATION
      );
      startTimeRef.current = null;
    }
  }, []);

  const reset = useCallback(() => {
    stop();
    setElapsedTime(0);
    pausedElapsedRef.current = 0;
    expiredRef.current = false;
    startTimeRef.current = null;
  }, [stop]);

  useEffect(() => {
    return () => {
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    };
  }, []);

  return { elapsedTime, isRunning, start, stop, reset };
}
