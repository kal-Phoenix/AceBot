import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { supabase } from '../lib/supabase';
import { telegram, TelegramUser } from '../lib/telegram';
import type { Database } from '../lib/database.types';

type DbUser = Database['public']['Tables']['users']['Row'];

interface AuthContextType {
  user: DbUser | null;
  telegramUser: TelegramUser | null;
  loading: boolean;
  signOut: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<DbUser | null>(null);
  const [telegramUser, setTelegramUser] = useState<TelegramUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    initAuth();
  }, []);

  async function initAuth() {
    try {
      telegram.init();

      const tgUser = telegram.getUser();
      setTelegramUser(tgUser);

      if (!tgUser) {
        setLoading(false);
        return;
      }

      const { data: existingUser } = await supabase
        .from('users')
        .select('*')
        .eq('telegram_user_id', tgUser.id)
        .maybeSingle();

      if (existingUser) {
        setUser(existingUser);
      } else {
        const newUser: Database['public']['Tables']['users']['Insert'] = {
          telegram_user_id: tgUser.id,
          username: tgUser.username || tgUser.first_name,
          first_name: tgUser.first_name,
          last_name: tgUser.last_name,
        };

        const { data: createdUser, error } = await supabase
          .from('users')
          .insert(newUser)
          .select()
          .single();

        if (error) {
          console.error('Error creating user:', error);
        } else {
          setUser(createdUser);
        }
      }
    } catch (error) {
      console.error('Auth initialization error:', error);
    } finally {
      setLoading(false);
    }
  }

  async function refreshUser() {
    if (!telegramUser) return;

    const { data } = await supabase
      .from('users')
      .select('*')
      .eq('telegram_user_id', telegramUser.id)
      .maybeSingle();

    if (data) {
      setUser(data);
    }
  }

  async function signOut() {
    setUser(null);
    setTelegramUser(null);
    telegram.close();
  }

  return (
    <AuthContext.Provider value={{ user, telegramUser, loading, signOut, refreshUser }}>
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
