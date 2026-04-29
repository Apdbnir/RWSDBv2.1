import { useState } from 'react';
import api from '../services/api';
import { useNotification } from '../context/NotificationContext';

const Backup = () => {
  const { success, error } = useNotification();
  const [creating, setCreating] = useState(false);
  const [backupHistory, setBackupHistory] = useState([]);

  const handleCreateBackup = async () => {
    try {
      setCreating(true);
      const result = await api.createBackup();
      
      // Add to history
      const historyItem = {
        path: result.backup_path || 'N/A',
        size: result.backup_size || 0,
        timestamp: result.timestamp || new Date().toISOString(),
        status: 'success',
      };
      setBackupHistory((prev) => [historyItem, ...prev]);
      
      success('Резервная копия создана успешно');
    } catch (err) {
      error('Ошибка при создании резервной копии');
      console.error(err);
      
      // Add failed attempt to history
      const historyItem = {
        path: 'N/A',
        size: 0,
        timestamp: new Date().toISOString(),
        status: 'failed',
      };
      setBackupHistory((prev) => [historyItem, ...prev]);
    } finally {
      setCreating(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">💾 Резервное копирование базы данных</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Backup Info & Actions */}
        <div>
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Информация</h3>
            <p className="text-gray-600 mb-4">
              Создайте полную копию базы данных для восстановления в случае необходимости. 
              Резервная копия включает все таблицы, данные, функции и триггеры.
            </p>
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
              <p className="text-sm text-yellow-800">
                <strong>⚠️ Важно:</strong> Для создания резервной копии требуются права суперпользователя 
                и установленный PostgreSQL pg_dump.
              </p>
            </div>
            <button
              onClick={handleCreateBackup}
              disabled={creating}
              className="btn btn-primary btn-large w-full disabled:opacity-50"
            >
              {creating ? (
                <>
                  <span className="animate-spin">⏳</span> Создание...
                </>
              ) : (
                <>
                  💾 Создать бэкап
                </>
              )}
            </button>
          </div>

          {/* Backup Tips */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">💡 Рекомендации</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2">
                <span className="text-green-500">✓</span>
                <span>Регулярно создавайте резервные копии (ежедневно или еженедельно)</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500">✓</span>
                <span>Храните копии в надежном месте (внешний диск, облако)</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500">✓</span>
                <span>Проверяйте целостность резервных копий</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500">✓</span>
                <span>Используйте автоматизацию для регулярного бэкапа</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Backup History */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📜 История бэкапов</h3>
          {backupHistory.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-2 px-3 text-sm font-semibold text-gray-700">Дата</th>
                    <th className="text-left py-2 px-3 text-sm font-semibold text-gray-700">Размер</th>
                    <th className="text-left py-2 px-3 text-sm font-semibold text-gray-700">Статус</th>
                  </tr>
                </thead>
                <tbody>
                  {backupHistory.map((item, index) => (
                    <tr key={index} className="border-b border-gray-100">
                      <td className="py-2 px-3 text-sm text-gray-600">
                        {new Date(item.timestamp).toLocaleString()}
                      </td>
                      <td className="py-2 px-3 text-sm text-gray-600">
                        {formatFileSize(item.size)}
                      </td>
                      <td className="py-2 px-3">
                        {item.status === 'success' ? (
                          <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded">
                            ✓ Успешно
                          </span>
                        ) : (
                          <span className="text-xs px-2 py-1 bg-red-100 text-red-700 rounded">
                            ✕ Ошибка
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="flex items-center justify-center h-48 text-gray-500">
              <div className="text-center">
                <span className="text-4xl block mb-2">📜</span>
                <p>История бэкапов пуста</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Backup;
