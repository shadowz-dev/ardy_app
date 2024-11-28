import { useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

export function useStorageState<T>(key: string, defaultValue?: T): [T | undefined, (value: T) => Promise<void>] {
  const [state, setState] = useState<T | undefined>(defaultValue);

  useEffect(() => {
    (async () => {
      try {
        const storedValue = await AsyncStorage.getItem(key);
        if (storedValue !== null) {
          setState(JSON.parse(storedValue));
        } else {
          setState(defaultValue);
        }
      } catch (error) {
        console.error(`Failed to load key "${key}" from AsyncStorage`, error);
      }
    })();
  }, [key]);

  const setValue = async (value: T) => {
    try {
      setState(value);
      await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(`Failed to save key "${key}" to AsyncStorage`, error);
    }
  };

  return [state, setValue];
}
