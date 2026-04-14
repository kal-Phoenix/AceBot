import { createContext, useContext, useEffect, useState } from 'react';
import { authAPI } from '../lib/api';
import WebApp from '@twa-dev/sdk';
import type { User, TelegramUser } from '../types';

type AuthContextType = {
  user: User | null;
  loading: boolean;
  signOut: () => Promise<void>;
  telegramUser: TelegramUser | null;
  updateUser: (userData: Partial<User>) => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [telegramUser, setTelegramUser] = useState<TelegramUser | null>(null);

  useEffect(() => {
    // Initialize Telegram WebApp
    WebApp.ready();
    WebApp.expand();
    
    // Set theme colors (only if supported)
    try {
      if (WebApp.version && parseFloat(WebApp.version) >= 6.1) {
        WebApp.setHeaderColor('#3b82f6');
        WebApp.setBackgroundColor('#f8fafc');
      }
    } catch (error) {
      // Ignore if not supported
      console.log('Theme colors not supported in this Telegram version');
    }

    // Authenticate with Telegram
    const authenticateWithTelegram = async () => {
      try {
        // Get Telegram user data
        const tgUser = WebApp.initDataUnsafe?.user;
        
        if (tgUser) {
          setTelegramUser(tgUser);
          
          // Authenticate with backend
          const data = await authAPI.telegramAuth(WebApp.initData, tgUser);
          
          // Save token
          localStorage.setItem('auth_token', data.token);
          
          // Get fresh user data from backend (includes stream from database)
          try {
            const userData = await authAPI.getMe();
            localStorage.setItem('user', JSON.stringify(userData));
            setUser(userData);
            console.log('User data loaded from backend:', userData);
            console.log('Profile picture URL:', userData.profile_picture);
          } catch (err) {
            console.error('Failed to get user data from backend:', err);
            // Fallback to auth response if /me fails
            localStorage.setItem('user', JSON.stringify(data.user));
            setUser(data.user);
            console.log('Using fallback user data:', data.user);
            console.log('Fallback profile picture URL:', data.user.profile_picture);
          }
        } else if (import.meta.env.DEV) {
          // For browser testing in development only - create mock Telegram user
          const mockTgUser: TelegramUser = {
            id: 123456789,
            first_name: 'Test',
            last_name: 'User',
            username: 'testuser',
            photo_url: 'https://ui-avatars.com/api/?name=Test+User&size=256&background=0ea5e9&color=fff&bold=true',
          };
          
          setTelegramUser(mockTgUser);
          
          // Authenticate with mock data
          const data = await authAPI.telegramAuth('', mockTgUser);
          
          // Save token
          localStorage.setItem('auth_token', data.token);
          
          // Get fresh user data from backend (includes stream from database)
          try {
            const userData = await authAPI.getMe();
            localStorage.setItem('user', JSON.stringify(userData));
            setUser(userData);
            console.log('User data loaded from backend (DEV):', userData);
            console.log('Profile picture URL (DEV):', userData.profile_picture);
          } catch (err) {
            console.error('Failed to get user data from backend (DEV):', err);
            // Fallback to auth response if /me fails
            localStorage.setItem('user', JSON.stringify(data.user));
            setUser(data.user);
            console.log('Using fallback user data (DEV):', data.user);
            console.log('Fallback profile picture URL (DEV):', data.user.profile_picture);
          }
        } else {
          throw new Error('Telegram user data not available');
        }
      } catch (error) {
        console.error('Telegram auth error:', error);
        // Try to load from localStorage as fallback
        const token = localStorage.getItem('auth_token');
        const savedUser = localStorage.getItem('user');
        
        if (token && savedUser) {
          try {
            // First use the saved user data immediately
            setUser(JSON.parse(savedUser));
            // Then try to get fresh data from backend
            const userData = await authAPI.getMe();
            setUser(userData);
            localStorage.setItem('user', JSON.stringify(userData));
          } catch (err) {
            // If backend fails, keep using the saved user data
            console.log('Using cached user data');
          }
        }
      } finally {
        setLoading(false);
      }
    };

    authenticateWithTelegram();
  }, []);

  const signOut = async () => {
    try {
      await authAPI.signOut();
    } catch (error) {
      console.error('Sign out error:', error);
    } finally {
      // Clear local storage and state
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      setUser(null);
      
      // Close the mini app
      WebApp.close();
    }
  };

  const updateUser = (userData: Partial<User>) => {
    setUser(prevUser => prevUser ? { ...prevUser, ...userData } : null);
    if (user) {
      localStorage.setItem('user', JSON.stringify({ ...user, ...userData }));
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, signOut, telegramUser, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}