import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LoginModal from '../components/LoginModal';
import api from '../services/api';

/**
 * Welcome/Landing Page for RWSDBv2.1
 * Belarusian Railway Station Database System
 */
const WelcomePage = () => {
  const navigate = useNavigate();
  const { isSuperUser } = useAuth();
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const handleTableClick = (table) => {
    navigate(`/databases?table=${table}`);
  };

  // Fetch database statistics on mount
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await api.getStatistics();
        setStats(data.statistics || []);
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  // Get count for a specific table
  const getTableCount = (tableName) => {
    if (!stats) return 0;
    const stat = stats.find(s => s.table === tableName);
    return stat ? stat.count : 0;
  };

  const features = [
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
      ),
      title: 'Табліцы',
      description: 'Перегляд усіх табліц базы дадзеных: пасажыры, цягнікі, квіткі, расклад',
      color: 'blue'
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      ),
      title: 'Пошук',
      description: 'Фільтрацыя і пошук запісаў па ўсіх палях',
      color: 'green'
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
      title: 'Статыстыка',
      description: 'Аналітыка і статыстыка па ўсіх табліцах',
      color: 'purple'
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
      title: 'Запыты',
      description: 'Спецыяльныя і ўласныя SQL-запыты',
      color: 'orange'
    }
  ];

  const handleEnterApp = () => {
    navigate('/app');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="absolute inset-0 bg-blue-600 blur-lg opacity-20 rounded-full"></div>
                <svg className="w-10 h-10 text-blue-600 relative" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  RWSDBv2.1
                </h1>
                <p className="text-xs text-gray-500 font-medium">Беларуская Чыгунка</p>
              </div>
            </div>
            {isSuperUser && (
              <div className="flex items-center gap-2 px-3 py-1.5 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Суперкарыстальнік
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Сістэма Кіравання
            <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Чыгуначнай Станцыяй
            </span>
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Сучасная інфармацыйная сістэма для кіравання дадзенымі Беларускай чыгункі
          </p>
          
          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button
              onClick={handleEnterApp}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 flex items-center gap-3"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
              Увайсці ў сістэму
            </button>
            {!isSuperUser && (
              <button
                onClick={() => setShowLoginModal(true)}
                className="px-8 py-4 bg-white border-2 border-purple-600 text-purple-600 rounded-lg font-semibold text-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 flex items-center gap-3"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
                Уваход для суперкарыстальніка
              </button>
            )}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-12 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 rounded-xl border border-gray-200 hover:border-blue-300 hover:shadow-lg transition-all duration-200 bg-gradient-to-br from-white to-gray-50"
              >
                <div className={`text-${feature.color}-600 mb-4`}>
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 text-sm">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Info Section */}
      <section className="py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white text-center shadow-xl mb-8">
            <h3 className="text-2xl font-bold mb-4">Рэжымы працы</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
              <div className="bg-white/10 rounded-lg p-4">
                <h4 className="font-semibold mb-2 flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  Карыстальнік
                </h4>
                <p className="text-sm text-blue-100">
                  Толькі прагляд дадзеных, пошук і фільтрацыя, выкананне запытаў
                </p>
              </div>
              <div className="bg-white/10 rounded-lg p-4">
                <h4 className="font-semibold mb-2 flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                  </svg>
                  Суперкарыстальнік
                </h4>
                <p className="text-sm text-blue-100">
                  Поўны доступ: дадаванне, змена, выдаленне запісаў, экспарт, рэзервовае капіраванне
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Database Statistics Section */}
      <section className="py-12 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-2xl font-bold text-center text-gray-900 mb-8">
            Статыстыка базы дадзеных
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {[
              { name: 'Пасажыры', table: 'passenger', icon: '👤' },
              { name: 'Цягнікі', table: 'train', icon: '🚂' },
              { name: 'Платформы', table: 'platform', icon: '🚉' },
              { name: 'Квіткі', table: 'ticket', icon: '🎫' },
              { name: 'Расклад', table: 'schedule', icon: '📅' },
              { name: 'Супрацоўнікі', table: 'employee', icon: '👨‍💼' },
              { name: 'Прызначэнні', table: 'work', icon: '📋' },
              { name: 'Паслугі', table: 'service', icon: '🛎️' },
              { name: 'Паслугі (прызначэнні)', table: 'appointment', icon: '✅' }
            ].map((item) => (
              <div
                key={item.table}
                onClick={() => handleTableClick(item.table)}
                className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-4 text-center hover:shadow-lg hover:scale-105 transition-all duration-200 border border-blue-100 cursor-pointer"
              >
                <div className="text-3xl mb-2">{item.icon}</div>
                <div className="text-sm text-gray-600 mb-1">{item.name}</div>
                {loading ? (
                  <div className="text-2xl font-bold text-blue-600 animate-pulse">...</div>
                ) : (
                  <div className="text-2xl font-bold text-blue-600">
                    {getTableCount(item.table)}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-sm">
            © 2026 RWSDBv2.1 - Belarusian Railway Station Database System
          </p>
          <p className="text-xs mt-2 text-gray-500">
            Сістэма распрацавана для кіравання дадзенымі Беларускай чыгункі
          </p>
        </div>
      </footer>

      {/* Login Modal */}
      <LoginModal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
      />
    </div>
  );
};

export default WelcomePage;
