import { useState, useCallback } from 'react';
import type { Character, GameConfig } from '../types';
import { filterCharacters, selectRandomCharacter } from '../services/characterService';

export function useCharacterSelection(config: GameConfig) {
  const [usedIds, setUsedIds] = useState<string[]>([]);
  const [pool] = useState<Character[]>(() => filterCharacters(config));

  const selectNext = useCallback((): Character | null => {
    const char = selectRandomCharacter(pool, usedIds);
    if (char) setUsedIds(prev => [...prev, char.id]);
    return char;
  }, [pool, usedIds]);

  const reset = useCallback(() => {
    setUsedIds([]);
  }, []);

  const remaining = pool.length - usedIds.length;

  return { selectNext, reset, remaining, poolSize: pool.length };
}
