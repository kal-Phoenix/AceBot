import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { telegram } from '../lib/telegram';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light');

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as Theme;
    const telegramTheme = telegram.colorScheme;

    const initialTheme = savedTheme || telegramTheme || 'light';
    setTheme(initialTheme);
    applyTheme(initialTheme);

    telegram.onThemeChanged(() => {
      const newTheme = telegram.colorScheme;
      if (newTheme === 'light' || newTheme === 'dark') {
        setTheme(newTheme);
        applyTheme(newTheme);
      }
    });
  }, []);

  function applyTheme(newTheme: Theme) {
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark');
      telegram.setHeaderColor('#1f2937');
      telegram.setBackgroundColor('#111827');
    } else {
      document.documentElement.classList.remove('dark');
      telegram.setHeaderColor('#ffffff');
      telegram.setBackgroundColor('#ffffff');
    }
  }

  function toggleTheme() {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
