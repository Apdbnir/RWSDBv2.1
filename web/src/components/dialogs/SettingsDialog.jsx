import { useState } from 'react';
import { useTheme } from '../../context/ThemeContext';
import { useLanguage } from '../../context/LanguageContext';

const SettingsMenu = ({ isOpen, onClose }) => {
  const { theme, toggleTheme, setThemeMode, isDark } = useTheme();
  const { language, setLanguage, t } = useLanguage();
  const [showLangMenu, setShowLangMenu] = useState(false);

  if (!isOpen) return null;

  const languages = [
    { code: 'be', name: 'Беларуская', flag: 'BY' },
    { code: 'ru', name: 'Русский', flag: 'RU' },
    { code: 'en', name: 'English', flag: 'GB' }
  ];

  const currentLang = languages.find(l => l.code === language);

  return (
    <>
      <div 
        className="fixed inset-0 z-40" 
        onClick={onClose}
      />
      <div className="absolute right-0 top-full mt-2 w-64 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50 overflow-hidden">
        {/* Theme Section */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
            {t('theme')}
          </h3>
          <div className="flex gap-2">
            <button
              onClick={() => setThemeMode('light')}
              className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
                theme === 'light'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              <span className="flex items-center justify-center gap-2">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                {t('lightTheme')}
              </span>
            </button>
            <button
              onClick={() => setThemeMode('dark')}
              className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
                theme === 'dark'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              <span className="flex items-center justify-center gap-2">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
                {t('darkTheme')}
              </span>
            </button>
          </div>
        </div>

        {/* Language Section */}
        <div className="p-4">
          <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
            {t('language')}
          </h3>
          <div className="relative">
            <button
              onClick={() => setShowLangMenu(!showLangMenu)}
              className="w-full py-2 px-3 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-medium flex items-center justify-between hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              <span className="flex items-center gap-2">
                <span className="text-lg">{currentLang?.flag === 'BY' ? '🇧🇾' : currentLang?.flag === 'RU' ? '🇷🇺' : '🇬🇧'}</span>
                {currentLang?.name}
              </span>
              <svg className={`w-4 h-4 transition-transform ${showLangMenu ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            {showLangMenu && (
              <div className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden z-10">
                {languages.map((lang) => (
                  <button
                    key={lang.code}
                    onClick={() => {
                      setLanguage(lang.code);
                      setShowLangMenu(false);
                    }}
                    className={`w-full py-2 px-3 text-left flex items-center gap-2 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors ${
                      language === lang.code ? 'bg-blue-50 dark:bg-blue-900 text-blue-600 dark:text-blue-400' : ''
                    }`}
                  >
                    <span className="text-lg">{lang.flag === 'BY' ? '🇧🇾' : lang.flag === 'RU' ? '🇷🇺' : '🇬🇧'}</span>
                    {lang.name}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default SettingsMenu;