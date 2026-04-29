import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [isSuperUser, setIsSuperUser] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user has superuser token on mount (session-based, not persistent)
    // Using sessionStorage instead of localStorage - clears on browser close/refresh
    const token = localStorage.getItem('superuser_token');
    setIsSuperUser(!!token);
    setIsLoading(false);

    // Listen for auth failures
    const handleAuthFailed = () => {
      setIsSuperUser(false);
      localStorage.removeItem('superuser_token');
    };

    window.addEventListener('auth-failed', handleAuthFailed);
    return () => window.removeEventListener('auth-failed', handleAuthFailed);
  }, []);

  const login = useCallback(async (password) => {
    try {
      await api.authenticate(password);
      // Use localStorage for persistent auth
      localStorage.setItem('superuser_token', password);
      setIsSuperUser(true);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.status === 401
          ? 'Неверный пароль'
          : 'Ошибка аутентификации'
      };
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('superuser_token');
    setIsSuperUser(false);
  }, []);

  const value = {
    isSuperUser,
    isLoading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
