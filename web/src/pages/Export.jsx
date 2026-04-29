import { useState } from 'react';
import api from '../services/api';
import { useNotification } from '../context/NotificationContext';

const Export = () => {
  const { success, error } = useNotification();
  const [selectedTable, setSelectedTable] = useState('');
  const [exportFormat, setExportFormat] = useState('json');
  const [useQuery, setUseQuery] = useState(false);
  const [customQuery, setCustomQuery] = useState('');
  const [exporting, setExporting] = useState(false);
  const [exportHistory, setExportHistory] = useState([]);

  const tables = [
    { name: 'schedule', label: 'Расклад' },
    { name: 'train', label: 'Цягнікі' },
    { name: 'platform', label: 'Платформы' },
    { name: 'passenger', label: 'Пасажыры' },
    { name: 'ticket', label: 'Білеты' },
    { name: 'employee', label: 'Супрацоўнікі' },
    { name: 'work', label: 'Работы' },
    { name: 'service', label: 'Паслугі' },
    { name: 'appointment', label: 'Назначэнні' },
  ];

  const handleExport = async () => {
    if (!selectedTable && !useQuery) {
      error('Выберите таблицу для экспорта');
      return;
    }

    if (useQuery && !customQuery.trim()) {
      error('Введите SQL запрос');
      return;
    }

    try {
      setExporting(true);
      
      // For now, we'll simulate export by fetching data and downloading
      let data;
      if (useQuery) {
        data = await api.executeQuery(customQuery);
      } else {
        data = await api.getTableData(selectedTable, {}, 10000, 0);
      }

      downloadData(data, exportFormat);
      
      // Add to history
      const historyItem = {
        table: useQuery ? 'Custom Query' : selectedTable,
        format: exportFormat,
        timestamp: new Date().toISOString(),
        records: data.count || 0,
      };
      setExportHistory((prev) => [historyItem, ...prev.slice(0, 9)]);
      
      success(`Экспорт выполнен: ${data.count} записей`);
    } catch (err) {
      error('Ошибка при экспорте данных');
      console.error(err);
    } finally {
      setExporting(false);
    }
  };

  const downloadData = (data, format) => {
    let content, mimeType, extension;

    if (format === 'json') {
      content = JSON.stringify(data.data, null, 2);
      mimeType = 'application/json';
      extension = 'json';
    } else if (format === 'csv') {
      content = convertToCSV(data);
      mimeType = 'text/csv';
      extension = 'csv';
    } else if (format === 'excel') {
      // For Excel, we'll create a CSV that Excel can open
      content = convertToCSV(data);
      mimeType = 'application/vnd.ms-excel';
      extension = 'xls';
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `export_${new Date().getTime()}.${extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const convertToCSV = (data) => {
    if (!data.data || data.data.length === 0) return '';

    const headers = data.columns || Object.keys(data.data[0]);
    const rows = data.data;

    const csvRows = [
      headers.join(','),
      ...rows.map((row) =>
        headers
          .map((header) => {
            const value = row[header];
            const escaped = String(value || '').replace(/"/g, '""');
            return `"${escaped}"`;
          })
          .join(',')
      ),
    ];

    return csvRows.join('\n');
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">📁 Экспорт данных</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Export Form */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Параметры экспорта</h3>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                📋 Таблица
              </label>
              <select
                className="select"
                value={selectedTable}
                onChange={(e) => setSelectedTable(e.target.value)}
                disabled={useQuery}
              >
                <option value="">-- Выберите таблицу --</option>
                {tables.map((table) => (
                  <option key={table.name} value={table.name}>
                    {table.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                📄 Формат
              </label>
              <select
                className="select"
                value={exportFormat}
                onChange={(e) => setExportFormat(e.target.value)}
              >
                <option value="json">JSON</option>
                <option value="csv">CSV</option>
                <option value="excel">Excel (XLS/XLSX)</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="useQuery"
                checked={useQuery}
                onChange={(e) => setUseQuery(e.target.checked)}
                className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
              />
              <label htmlFor="useQuery" className="text-sm text-gray-700">
                📝 Использовать SQL запрос
              </label>
            </div>

            {useQuery && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  SQL запрос
                </label>
                <textarea
                  className="w-full h-32 p-3 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none resize-none"
                  placeholder="SELECT * FROM employee LIMIT 100;"
                  value={customQuery}
                  onChange={(e) => setCustomQuery(e.target.value)}
                />
              </div>
            )}

            <button
              onClick={handleExport}
              disabled={exporting || (!selectedTable && !useQuery)}
              className="btn btn-primary btn-large w-full disabled:opacity-50"
            >
              {exporting ? (
                <>
                  <span className="animate-spin">⏳</span> Экспорт...
                </>
              ) : (
                <>
                  📥 Экспортировать
                </>
              )}
            </button>
          </div>
        </div>

        {/* Export History */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📜 История экспорта</h3>
          {exportHistory.length > 0 ? (
            <div className="space-y-3">
              {exportHistory.map((item, index) => (
                <div
                  key={index}
                  className="p-3 bg-gray-50 rounded-lg border border-gray-200"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium text-gray-800">{item.table}</span>
                    <span className="text-xs px-2 py-1 bg-primary-100 text-primary-700 rounded">
                      {item.format.toUpperCase()}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600">
                    {item.records} записей • {new Date(item.timestamp).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex items-center justify-center h-48 text-gray-500">
              <div className="text-center">
                <span className="text-4xl block mb-2">📜</span>
                <p>История экспорта пуста</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Export;
