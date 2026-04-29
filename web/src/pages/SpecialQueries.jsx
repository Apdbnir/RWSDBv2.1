import { useState } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import { useNotification } from '../context/NotificationContext';

const SpecialQueries = () => {
  const { success, error } = useNotification();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const specialQueries = {
    stats: [
      { label: 'Колькасць запісаў у табліцах', query: 'statistics' },
      { label: 'Тыпы цягнікоў і іх колькасць', query: 'train_types' },
      { label: 'Статыстыка па станцыях', query: 'station_stats' },
    ],
    schedule: [
      { label: 'Расклад цягнікоў на сёння', query: 'today_schedule' },
      { label: 'Бліжэйшыя адпраўленні', query: 'next_departures' },
    ],
    train: [
      { label: 'Хуткія цягнікі (>150 км/ч)', query: 'fast_trains' },
    ],
    employee: [
      { label: 'Супрацоўнікі паводле пасад', query: 'employee_positions' },
    ],
    service: [
      { label: 'Паслугі паводле тыпаў', query: 'service_types' },
    ],
    advanced: [
      { label: 'Аналіз продажаў білетаў', query: 'ticket_sales' },
      { label: 'Загружанасць платформ', query: 'platform_load' },
    ],
  };

  const handleExecuteQuery = async (queryLabel, queryName) => {
    try {
      setLoading(true);
      const data = await api.executeQuery(queryName);
      setResult({ label: queryLabel, ...data });
      success(`Выканана. Знойдзена запісаў: ${data.count || 0}`);
    } catch (err) {
      error('Памылка выканання запыту: ' + (err.message || err));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderQuerySection = (title, queries) => (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">{title}</h3>
      <div className="space-y-2">
        {queries.map((q, index) => (
          <button
            key={index}
            onClick={() => handleExecuteQuery(q.label, q.query)}
            disabled={loading}
            className="w-full text-left px-4 py-3 bg-gray-50 hover:bg-blue-50 rounded-lg transition-colors text-sm text-gray-700 hover:text-blue-700 disabled:opacity-50 border border-gray-200 hover:border-blue-300"
          >
            {q.label}
          </button>
        ))}
      </div>
    </div>
  );

  const columns = result?.columns
    ? result.columns.map((col) => ({
        key: col,
        label: col,
        render: (value) => {
          if (value === null) return <span className="text-gray-400">null</span>;
          if (typeof value === 'boolean') return value ? '✓' : '✗';
          return String(value);
        },
      }))
    : [];

  return (
    <div className="flex h-[calc(100vh-8rem)] overflow-hidden">
      {/* Left Panel - Query Buttons */}
      <div className="w-1/3 min-w-80 bg-gray-50 border-r border-gray-200 overflow-y-auto p-4">
        <h2 className="text-xl font-bold text-gray-800 mb-2 flex items-center gap-2">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          Спецзапыты
        </h2>
        <p className="text-sm text-gray-600 mb-4">Абярыце запыт для выканання</p>

        <div className="space-y-4">
          {renderQuerySection(
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Статыстыка
            </span>,
            specialQueries.stats
          )}
          {renderQuerySection(
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Расклад
            </span>,
            specialQueries.schedule
          )}
          {renderQuerySection(
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Цягнікі
            </span>,
            specialQueries.train
          )}
          {renderQuerySection(
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Супрацоўнікі
            </span>,
            specialQueries.employee
          )}
          {renderQuerySection(
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M9 3h.01M12 3h.01M15 3h.01M21 21v-7a2 2 0 00-2-2H5a2 2 0 00-2 2v7h18zm-3-9v-2a2 2 0 00-2-2H8a2 2 0 00-2 2v2h12z" />
              </svg>
              Паслугі
            </span>,
            specialQueries.service
          )}
          {renderQuerySection(
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Прасунутая аналітыка
            </span>,
            specialQueries.advanced
          )}
        </div>
      </div>

      {/* Right Panel - Results */}
      <div className="flex-1 overflow-hidden flex flex-col">
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Вынік выканання
          </h2>
        </div>

        <div className="flex-1 overflow-auto p-6">
          {loading ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              <svg className="animate-spin h-12 w-12" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              <span className="ml-4">Выкананне запыту...</span>
            </div>
          ) : result ? (
            <DataTable columns={columns} data={result.data || []} />
          ) : (
            <div className="flex items-center justify-center h-full text-gray-400">
              <svg className="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span className="text-lg">Абярыце запыт для выканання</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SpecialQueries;
