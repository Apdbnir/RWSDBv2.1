import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { useNotification } from '../context/NotificationContext';
import SettingsDialog from './dialogs/SettingsDialog';

const Header = ({ onLoginClick }) => {
  const { isSuperUser, logout } = useAuth();
  const { showNotification } = useNotification();
  const [dbType, setDbType] = useState('postgresql');
  const [isSwitching, setIsSwitching] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  // Fetch config on mount and periodically
  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const config = await api.getConfig();
        setDbType(config.database_type);
      } catch (error) {
        console.error('Failed to fetch config:', error);
      }
    };
    fetchConfig();
    // Poll every 2 seconds for DB type changes
    const interval = setInterval(fetchConfig, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleDbSwitch = async (newType) => {
    if (newType === dbType) return;
    
    setIsSwitching(true);
    try {
      const result = await api.updateConfig({ database_type: newType });
      if (result.success) {
        setDbType(result.database_type);
        showNotification(`База данных переключена на ${newType === 'postgresql' ? 'PostgreSQL' : 'BerkeleyDB'}`, 'success');
        // Reload page to refresh all data from the new DB
        setTimeout(() => window.location.reload(), 1000);
      } else {
        showNotification('Не удалось переключить базу данных', 'error');
      }
    } catch (error) {
      showNotification(`Ошибка при переключении: ${error.message}`, 'error');
    } finally {
      setIsSwitching(false);
    }
  };

  return (
    <header className="bg-white shadow-lg border-b border-gray-200 sticky top-0 z-40 backdrop-blur-sm bg-opacity-95">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Title */}
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="absolute inset-0 bg-blue-600 blur-lg opacity-20 rounded-full"></div>
              <svg className="w-10 h-10 text-blue-600 relative" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">RWSDBv2.1</h1>
              <p className="text-xs text-gray-500 font-medium">Беларуская Чыгунка</p>
            </div>
          </div>

          {/* DB Switcher and User Info */}
          <div className="flex items-center gap-6">
            {/* DB Switcher - Always visible */}
            <div className="flex items-center bg-gray-100 dark:bg-gray-700 p-1 rounded-lg border border-gray-200 dark:border-gray-600">
              <button
                onClick={() => handleDbSwitch('postgresql')}
                disabled={isSwitching}
                className={`px-4 py-2 text-sm font-bold rounded-md transition-all flex items-center gap-2 ${
                  dbType === 'postgresql' 
                    ? 'bg-blue-600 text-white shadow-sm' 
                    : 'text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                } ${isSwitching ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                </svg>
                PostgreSQL
              </button>
              <button
                onClick={() => handleDbSwitch('berkeleydb')}
                disabled={isSwitching}
                className={`px-4 py-2 text-sm font-bold rounded-md transition-all flex items-center gap-2 ${
                  dbType === 'berkeleydb' 
                    ? 'bg-green-600 text-white shadow-sm' 
                    : 'text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                } ${isSwitching ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                BerkeleyDB
              </button>
            </div>

            <div className="h-6 w-px bg-gray-200"></div>

            {/* Settings Button */}
            <div className="relative">
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="p-2 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors"
                title="Settings"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
              <SettingsDialog isOpen={showSettings} onClose={() => setShowSettings(false)} />
            </div>

            {isSuperUser ? (
              <div className="flex items-center gap-3">
                <div className="hidden sm:flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-100 to-purple-200 text-purple-800 rounded-full text-sm font-semibold shadow-sm border border-purple-300">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                  </svg>
                  <span>Суперпользователь</span>
                </div>
                <button
                  onClick={logout}
                  className="btn btn-secondary btn-sm flex items-center gap-2 hover:shadow-md transition-all duration-200"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  <span className="hidden sm:inline">Выйти</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <div className="hidden sm:flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 rounded-full text-sm font-semibold shadow-sm border border-gray-300">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <span>Пользователь</span>
                </div>
                <button
                  onClick={onLoginClick}
                  className="btn btn-primary btn-sm flex items-center gap-2 hover:shadow-lg transition-all duration-200 transform hover:scale-105"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                  </svg>
                  <span className="hidden sm:inline">Войти</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
