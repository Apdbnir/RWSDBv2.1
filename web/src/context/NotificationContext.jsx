import { createContext, useContext, useState, useCallback } from 'react';

const NotificationContext = createContext(null);

export const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotification must be used within a NotificationProvider');
  }
  return context;
};

export const NotificationProvider = ({ children }) => {
  const [notification, setNotification] = useState(null);

  const showNotification = useCallback((message, type = 'info', duration = 3000) => {
    setNotification({ message, type });
    
    if (duration > 0) {
      setTimeout(() => {
        setNotification(null);
      }, duration);
    }
  }, []);

  const hideNotification = useCallback(() => {
    setNotification(null);
  }, []);

  const success = useCallback((message, duration) => {
    showNotification(message, 'success', duration);
  }, [showNotification]);

  const error = useCallback((message, duration) => {
    showNotification(message, 'error', duration);
  }, [showNotification]);

  const info = useCallback((message, duration) => {
    showNotification(message, 'info', duration);
  }, [showNotification]);

  const value = {
    notification,
    showNotification,
    hideNotification,
    success,
    error,
    info,
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
};
