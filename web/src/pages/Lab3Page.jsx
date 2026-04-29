import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';
import api from '../services/api';

/**
 * BerkeleyDB Converter
 * PostgreSQL to BerkeleyDB conversion interface
 */
const Lab3Page = () => {
  const { isSuperUser } = useAuth();
  const { success, error } = useNotification();
  const [converting, setConverting] = useState(false);
  const [result, setResult] = useState(null);
  const [logs, setLogs] = useState([]);

  const handleConvert = async () => {
    if (!isSuperUser) {
      error('Толькі суперкарыстальнік можа выконваць канвертацыю');
      return;
    }

    setConverting(true);
    setResult(null);
    setLogs([]);

    try {
      // Add initial log
      setLogs(prev => [...prev, 'Пачатак канвертацыі...']);

      const result = await api.lab3Convert();
      console.log('Conversion result:', result);

      // Check for success field or tables_converted
      if (result.tables_converted !== undefined || result.success) {
        setResult(result);
        setLogs(prev => [
          ...prev,
          `✓ Канвертацыя завершана`,
          `✓ Табліц канвертавана: ${result.tables_converted}`,
          `✓ Усяго запісаў: ${result.total_records}`,
          `✓ Выніковая папка: ${result.output_dir}`
        ]);
        success('Канвертацыя BerkeleyDB завершана паспяхова!');
      } else {
        throw new Error(result.error || 'Памылка канвертацыі');
      }
    } catch (err) {
      const errorMsg = err.message || 'Невядомая памылка';
      setLogs(prev => [...prev, `✗ Памылка: ${errorMsg}`]);
      error(`Памылка канвертацыі: ${errorMsg}`);
    } finally {
      setConverting(false);
    }
  };

  const tables = [
    { name: 'passenger', key: 'passenger_number', description: 'Пасажыры' },
    { name: 'train', key: 'train_number', description: 'Цягнікі' },
    { name: 'platform', key: 'platform_number', description: 'Платформы' },
    { name: 'ticket', key: 'ticket_number', description: 'Квіткі' },
    { name: 'schedule', key: 'schedule_number', description: 'Расклад' },
    { name: 'employee', key: 'employee_number', description: 'Супрацоўнікі' },
    { name: 'service', key: 'service_number', description: 'Паслугі' }
  ];

  return (
    <div className="p-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Канвертар базы даных
        </h1>
        <p className="text-gray-600">
          PostgreSQL → BerkeleyDB
        </p>
      </div>

      {/* Info Card */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
        <h2 className="text-lg font-semibold text-blue-900 mb-3">
          Прызначэнне
        </h2>
        <ul className="space-y-2 text-blue-800">
          <li className="flex items-start gap-2">
            <span className="text-blue-600 mt-1">•</span>
            <span>Канвертацыя табліц PostgreSQL у фармат BerkeleyDB</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-600 mt-1">•</span>
            <span>Выкарыстанне першасных ключоў як ключоў BerkeleyDB</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-600 mt-1">•</span>
            <span>Серыялізацыя значэнняў у JSON фармат</span>
          </li>
        </ul>
      </div>

      {/* Technical Requirements */}
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Тэхнічныя патрабаванні
        </h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Табліца PostgreSQL</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ключ BerkeleyDB</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Значэнне (JSON)</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {tables.map((table) => (
                <tr key={table.name}>
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">{table.name}</td>
                  <td className="px-4 py-3 text-sm text-gray-600 font-mono">{table.key}</td>
                  <td className="px-4 py-3 text-sm text-gray-600 font-mono text-xs">
                    {`{${table.name}, ...}`}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Conversion Control */}
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Канвертацыя даных
        </h2>
        
        {!isSuperUser ? (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800 flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              Для выканання канвертацыі неабходны правы суперкарыстальніка
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <button
              onClick={handleConvert}
              disabled={converting}
              className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center gap-3 ${
                converting
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg'
              }`}
            >
              {converting ? (
                <>
                  <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Канвертацыя...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.058M5.05 5.05A21 21 0 0112 3a21 21 0 0121 21m0-21a21 21 0 01-21 21m-5.05-5.05A21 21 0 013 12a21 21 0 0121-21m0 21a21 21 0 01-21-21m5.05-5.05A21 21 0 0112 21a21 21 0 01-21-21m0 21a21 21 0 0121-21" />
                  </svg>
                  Запусціць канвертацыю
                </>
              )}
            </button>

            {/* Logs */}
            {logs.length > 0 && (
              <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm text-green-400 max-h-64 overflow-y-auto">
                {logs.map((log, index) => (
                  <div key={index} className="py-1">
                    {log}
                  </div>
                ))}
              </div>
            )}

            {/* Result */}
            {result && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h3 className="font-semibold text-green-900 mb-3">Вынікі канвертацыі</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-white rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-green-600">{result.tables_converted}</div>
                    <div className="text-xs text-gray-600">Табліц</div>
                  </div>
                  <div className="bg-white rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-green-600">{result.total_records}</div>
                    <div className="text-xs text-gray-600">Запісаў</div>
                  </div>
                  <div className="bg-white rounded-lg p-3 text-center">
                    <div className="text-xs text-gray-600">Папка</div>
                    <div className="text-xs font-mono text-gray-800 truncate">{result.output_dir}</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Algorithm */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Алгарытм канвертара
        </h2>
        <ol className="space-y-3">
          <li className="flex items-start gap-3">
            <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">1</span>
            <span className="text-gray-700">Падключэнне да базы даных PostgreSQL</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">2</span>
            <span className="text-gray-700">Атрыманне інфармацыі аб табліцах (назвы, слупкі, змест)</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">3</span>
            <span className="text-gray-700">Стварэнне баз даных BerkeleyDB і іх запаўненне</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">4</span>
            <span className="text-gray-700">Закрыццё злучэнняў з базамі даных</span>
          </li>
        </ol>
      </div>
    </div>
  );
};

export default Lab3Page;
