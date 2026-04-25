import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import api from '../services/api';
import { User } from '../types';

interface AuthContextValue {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<User>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('access_token'));
  const [loading, setLoading] = useState<boolean>(!!localStorage.getItem('access_token'));

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }
    api.get<User>('/auth/me')
      .then((res) => setUser(res.data))
      .catch(() => {
        localStorage.removeItem('access_token');
        setToken(null);
      })
      .finally(() => setLoading(false));
  }, [token]);

  const login = useCallback(async (email: string, password: string): Promise<User> => {
    const res = await api.post<{ access_token: string; token_type: string }>('/auth/login', { email, password });
    const newToken = res.data.access_token;
    localStorage.setItem('access_token', newToken);
    setToken(newToken);
    const meRes = await api.get<User>('/auth/me');
    setUser(meRes.data);
    return meRes.data;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    setToken(null);
    setUser(null);
  }, []);

  const value = useMemo(() => ({ user, token, loading, login, logout }), [user, token, loading, login, logout]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
