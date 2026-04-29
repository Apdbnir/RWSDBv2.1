import { useState } from 'react';
import api from '../services/api';
import DataTable from '../components/DataTable';
import { useNotification } from '../context/NotificationContext';

const Queries = () => {
  const { success, error } = useNotification();
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [queryHistory, setQueryHistory] = useState([]);

  const presetQueries = [
    {
      label: 'Все супрацоўнікі',
      query: 'SELECT * FROM employee LIMIT 100;',
    },
    {
      label: 'Все цягнікі',
      query: 'SELECT * FROM train LIMIT 100;',
    },
    {
      label: 'Все пасажыры',
      query: 'SELECT * FROM passenger LIMIT 100;',
    },
    {
      label: 'Все білеты',
      query: 'SELECT * FROM ticket LIMIT 100;',
    },
    {
      label: 'Расклад',
      query: 'SELECT * FROM schedule LIMIT 100;',
    },
    {
      label: 'Платформы',
      query: 'SELECT * FROM platform;',
    },
    {
      label: 'Паслугі',
      query: 'SELECT * FROM service;',
    },
    {
      label: 'Работы',
      query: 'SELECT * FROM work LIMIT 100;',
    },
    {
      label: 'Назначэнні',
      query: 'SELECT * FROM appointment LIMIT 100;',
    },
  ];

  const handleExecuteQuery = async () => {
    if (!query.trim()) {
      error('Введите SQL запрос');
      return;
    }

    if (!query.trim().toUpperCase().startsWith('SELECT')) {
      error('Разрешены только SELECT запросы');
      return;
    }

    try {
      setLoading(true);
      const data = await api.executeQuery(query);
      setResult(data);
      
      // Add to history
      setQueryHistory((prev) => [query, ...prev.slice(0, 9)]);
      success(`Выполнено. Найдено записей: ${data.count || 0}`);
    } catch (err) {
      error('Ошибка выполнения запроса');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleClearQuery = () => {
    setQuery('');
    setResult(null);
  };

  const handlePresetClick = (presetQuery) => {
    setQuery(presetQuery);
  };

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
    <div className="p-6 h-[calc(100vh-8rem)] overflow-y-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">💻 Выполнение SQL запросов</h2>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
        {/* Preset Queries */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-4">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📑 Готовые запросы</h3>
            <div className="space-y-2">
              {presetQueries.map((preset, index) => (
                <button
                  key={index}
                  onClick={() => handlePresetClick(preset.query)}
                  className="w-full text-left px-3 py-2 bg-gray-50 hover:bg-primary-50 rounded-lg transition-colors text-sm text-gray-700 hover:text-primary-700"
                >
                  {preset.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Query Editor */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow-md p-4 mb-4">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">✏️ SQL редактор</h3>
            <textarea
              className="w-full h-40 p-4 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none resize-none"
              placeholder="Введите SQL запрос (только SELECT)...&#10;&#10;Прыклад:&#10;SELECT * FROM employee LIMIT 10;"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <div className="flex items-center gap-3 mt-4">
              <button
                onClick={handleExecuteQuery}
                disabled={loading || !query.trim()}
                className="btn btn-primary disabled:opacity-50"
              >
                ▶ Выполнить
              </button>
              <button onClick={handleClearQuery} className="btn btn-secondary">
                🗑 Очистить
              </button>
            </div>
          </div>

          {/* Query Results */}
          <div className="bg-white rounded-lg shadow-md p-4">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">📊 Результат</h3>
            {loading ? (
              <div className="flex items-center justify-center h-40 text-gray-500">
                <span className="text-2xl animate-spin">⏳</span>
                <span className="ml-3">Выполнение...</span>
              </div>
            ) : result ? (
              <div>
                <div className="mb-4 text-sm text-gray-600">
                  Найдено записей: <span className="font-semibold">{result.count}</span>
                </div>
                <div className="overflow-x-auto max-h-96 overflow-y-auto">
                  <DataTable columns={columns} data={result.data} canEdit={false} canDelete={false} />
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-40 text-gray-500">
                <div className="text-center">
                  <span className="text-4xl block mb-2">📝</span>
                  <p>Результат запроса появится здесь</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Query History */}
      {queryHistory.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📜 История запросов</h3>
          <div className="space-y-2">
            {queryHistory.map((q, index) => (
              <button
                key={index}
                onClick={() => setQuery(q)}
                className="w-full text-left px-3 py-2 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors text-sm font-mono text-gray-700 truncate"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Queries;
