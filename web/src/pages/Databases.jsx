import { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../services/api';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';

const Databases = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const { isSuperUser } = useAuth();
  const { success, error } = useNotification();

  const [selectedTable, setSelectedTable] = useState(searchParams.get('table') || 'employee');
  const [tableData, setTableData] = useState({ columns: [], data: [] });
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('');
  const [page, setPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingRecord, setEditingRecord] = useState(null);
  const [formData, setFormData] = useState({});
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [selectedRows, setSelectedRows] = useState([]);
  const [focusedRowIndex, setFocusedRowIndex] = useState(0);

  // Helper functions for keyboard shortcuts
  const handleDeleteAction = () => {
    if (selectedRows.length > 0) {
      // Delete multiple selected rows
      setConfirmDelete(selectedRows[0]);
    } else if (tableData.data.length > 0) {
      // Select first row and delete
      setConfirmDelete(tableData.data[0]);
    }
  };

  const handleEditAction = () => {
    if (selectedRows.length > 0) {
      // Edit first selected row
      handleEditRecord(selectedRows[0]);
    } else if (tableData.data.length > 0) {
      // Edit first row
      handleEditRecord(tableData.data[0]);
    }
  };

  // Keyboard shortcuts handler
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ignore when typing in inputs/dialogs
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
        return;
      }

      const key = e.key.toLowerCase();

      // D - Delete selected record(s) - Superuser only
      if (key === 'd' && isSuperUser) {
        e.preventDefault();
        e.stopImmediatePropagation();
        handleDeleteAction();
        return false;
      }

      // U - Update selected record - Superuser only
      if (key === 'u' && isSuperUser) {
        e.preventDefault();
        e.stopImmediatePropagation();
        handleEditAction();
        return false;
      }

      // A - Add new record - Superuser only
      if (key === 'a' && isSuperUser) {
        e.preventDefault();
        e.stopImmediatePropagation();
        handleAddRecord();
        return false;
      }

      // V - Refresh table
      if (key === 'v') {
        e.preventDefault();
        e.stopImmediatePropagation();
        loadTableData();
        return false;
      }

      // Space - Select/deselect focused row
      if (key === ' ') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (tableData.data.length > 0 && focusedRowIndex < tableData.data.length) {
          handleRowSelect(tableData.data[focusedRowIndex], false);
        }
        return false;
      }

      // Enter - Edit focused row - Superuser only
      if (key === 'enter' && isSuperUser) {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (tableData.data.length > 0 && focusedRowIndex < tableData.data.length) {
          handleEditRecord(tableData.data[focusedRowIndex]);
        }
        return false;
      }
    };

    document.addEventListener('keydown', handleKeyDown, true);
    return () => document.removeEventListener('keydown', handleKeyDown, true);
  }, [selectedRows, tableData, focusedRowIndex, isSuperUser]);

  const renderTableIcon = (iconName) => {
    const icons = {
      schedule: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      ),
      train: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
      platform: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      ),
      passenger: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      ),
      ticket: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
        </svg>
      ),
      employee: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
      work: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z" />
        </svg>
      ),
      service: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M9 3h.01M12 3h.01M15 3h.01M21 21v-7a2 2 0 00-2-2H5a2 2 0 00-2 2v7h18zm-3-9v-2a2 2 0 00-2-2H8a2 2 0 00-2 2v2h12z" />
        </svg>
      ),
      appointment: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      ),
    };
    return icons[iconName] || null;
  };

  const tables = [
    { name: 'schedule', label: 'Расклад', icon: 'schedule' },
    { name: 'train', label: 'Цягнікі', icon: 'train' },
    { name: 'platform', label: 'Платформы', icon: 'platform' },
    { name: 'passenger', label: 'Пасажыры', icon: 'passenger' },
    { name: 'ticket', label: 'Білеты', icon: 'ticket' },
    { name: 'employee', label: 'Супрацоўнікі', icon: 'employee' },
    { name: 'work', label: 'Работы', icon: 'work' },
    { name: 'service', label: 'Паслугі', icon: 'service' },
    { name: 'appointment', label: 'Назначэнні', icon: 'appointment' },
  ];

  const PAGE_SIZE = 20;

  const isLookupTable = api.isLookupTable(selectedTable);
  // Only superuser can modify any table
  const canModify = isSuperUser;

  useEffect(() => {
    loadTableData();
    setSelectedRows([]); // Clear selection on table/filter/page change
    setFocusedRowIndex(0); // Reset focus on table/filter/page change
  }, [selectedTable, page, filter]);

  const loadTableData = async () => {
    try {
      setLoading(true);
      // Smart filter - search in all text columns
      const filters = {};
      if (filter) {
        // Get first text column for filtering
        const textColumns = tableData.columns.filter(col => 
          !col.includes('_id') && !col.includes('_number') && !col.includes('created') && !col.includes('updated')
        );
        if (textColumns.length > 0) {
          filters[textColumns[0]] = filter;
        }
      }
      const data = await api.getTableData(
        selectedTable,
        filters,
        PAGE_SIZE,
        (page - 1) * PAGE_SIZE
      );
      setTableData(data);
      setTotalRecords(data.count || 0);
    } catch (err) {
      error('Памылка загрузкі даных');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTableSelect = (tableName) => {
    setSelectedTable(tableName);
    setSearchParams({ table: tableName });
    setPage(1);
    setFilter('');
  };

  const handleAddRecord = () => {
    setEditingRecord(null);
    setFormData({});
    setIsModalOpen(true);
  };

  const handleEditRecord = (record) => {
    setEditingRecord(record);
    setFormData({ ...record });
    setIsModalOpen(true);
  };

  const handleDeleteRecord = (record) => {
    setConfirmDelete(record);
  };

  const handleRowSelect = (row, isMultiSelect) => {
    if (isMultiSelect) {
      // Ctrl+click - toggle selection
      const rowId = row[getIdColumn()];
      const isSelected = selectedRows.some(r => r[getIdColumn()] === rowId);
      if (isSelected) {
        setSelectedRows(selectedRows.filter(r => r[getIdColumn()] !== rowId));
      } else {
        setSelectedRows([...selectedRows, row]);
      }
    } else {
      // Regular click - select single row
      setSelectedRows([row]);
    }
  };

  const confirmDeleteRecord = async () => {
    try {
      const idColumn = getIdColumn();
      // Delete selected rows if any, otherwise delete the confirmDelete record
      const rowsToDelete = selectedRows.length > 0 ? selectedRows : [confirmDelete];
      
      for (const row of rowsToDelete) {
        await api.deleteRecord(selectedTable, row[idColumn]);
      }
      
      success(`Удалено записей: ${rowsToDelete.length}`);
      setSelectedRows([]);
      loadTableData();
    } catch (err) {
      error('Ошибка при удалении');
      console.error(err);
    } finally {
      setConfirmDelete(null);
    }
  };

  const handleSaveRecord = async () => {
    try {
      if (editingRecord) {
        const idColumn = getIdColumn();
        await api.updateRecord(selectedTable, editingRecord[idColumn], formData);
        success('Запись обновлена');
      } else {
        await api.createRecord(selectedTable, formData);
        success('Запись создана');
      }
      setIsModalOpen(false);
      loadTableData();
    } catch (err) {
      error('Ошибка при сохранении');
      console.error(err);
    }
  };

  const getIdColumn = useCallback(() => {
    // Dynamically get primary key for the selected table
    return api.getPrimaryKey(selectedTable);
  }, [selectedTable]);

  const columns = tableData.columns
    .filter((col) => col !== 'created_at' && col !== 'updated_at')
    .map((col) => ({
      key: col,
      label: col,
      render: (value) => {
        if (value === null) return <span className="text-gray-400">null</span>;
        if (typeof value === 'boolean') return value ? '✓' : '✗';
        return String(value);
      },
    }));

  const renderFormFields = () => {
    return tableData.columns
      .filter((col) => col !== 'created_at' && col !== 'updated_at')
      .map((col) => (
        <div key={col} className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {col}
          </label>
          <input
            type="text"
            className="input"
            value={formData[col] || ''}
            onChange={(e) => setFormData({ ...formData, [col]: e.target.value })}
            placeholder={`Введите ${col}`}
          />
        </div>
      ));
  };

  return (
    <div className="flex h-[calc(100vh-8rem)]">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 overflow-y-auto">
        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            Базы даных
          </h3>
          <div className="space-y-1">
            {tables.map((table) => (
              <button
                key={table.name}
                onClick={() => handleTableSelect(table.name)}
                className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                  selectedTable === table.name
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <span className="text-gray-500">
                  {renderTableIcon(table.icon)}
                </span>
                <span className="text-sm font-medium">{table.label}</span>
                {api.isLookupTable(table.name) && (
                  <span className="ml-auto text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded flex items-center gap-1">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <section className="flex-1 overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <h2 className="text-xl font-bold text-gray-800">
                {tables.find((t) => t.name === selectedTable)?.label || selectedTable}
              </h2>
              {selectedRows.length > 0 && (
                <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                  Выделено: {selectedRows.length}
                </span>
              )}
            </div>
            <div className="flex items-center gap-3">
              <input
                type="text"
                className="input w-64"
                placeholder="Фильтр..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
              />
              <button onClick={loadTableData} className="btn btn-secondary" title="Обновить">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.058M5.05 5.05A21 21 0 0112 3a21 21 0 0121 21m0-21a21 21 0 01-21 21m-5.05-5.05A21 21 0 013 12a21 21 0 0121-21m0 21a21 21 0 01-21-21m5.05-5.05A21 21 0 0112 21a21 21 0 01-21-21m0 21a21 21 0 0121-21" />
                </svg>
              </button>
              {canModify && (
                <button onClick={handleAddRecord} className="btn btn-primary">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  Добавить
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="flex-1 overflow-y-auto p-4">
          {loading ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              <svg className="animate-spin h-8 w-8" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              <span className="ml-3">Загрузка...</span>
            </div>
          ) : (
            <DataTable
              columns={columns}
              data={tableData.data}
              onEdit={canModify ? handleEditRecord : null}
              onDelete={canModify ? handleDeleteRecord : null}
              canEdit={canModify}
              canDelete={canModify}
              selectedRows={selectedRows}
              onRowSelect={handleRowSelect}
              focusedRowIndex={focusedRowIndex}
              onFocusedRowChange={setFocusedRowIndex}
            />
          )}
        </div>

        {/* Footer */}
        <div className="bg-white border-t border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">
              Записей: {totalRecords}
            </span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
                className="btn btn-secondary btn-sm disabled:opacity-50"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Назад
              </button>
              <span className="text-sm text-gray-600">
                Стр. {page}
              </span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={tableData.data.length < PAGE_SIZE}
                className="btn btn-secondary btn-sm disabled:opacity-50"
              >
                Вперед
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Add/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={
          <span className="flex items-center gap-2">
            {editingRecord ? (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            )}
            {editingRecord ? 'Редактировать запись' : 'Добавить запись'}
          </span>
        }
        size="md"
        actions={
          <>
            <button onClick={() => setIsModalOpen(false)} className="btn btn-secondary">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Отмена
            </button>
            <button onClick={handleSaveRecord} className="btn btn-primary">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
              </svg>
              Сохранить
            </button>
          </>
        }
      >
        <form onSubmit={(e) => e.preventDefault()}>{renderFormFields()}</form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={!!confirmDelete}
        onClose={() => setConfirmDelete(null)}
        title={
          <span className="flex items-center gap-2 text-red-600">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Подтверждение удаления
          </span>
        }
        size="sm"
        actions={
          <>
            <button onClick={() => setConfirmDelete(null)} className="btn btn-secondary">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Отмена
            </button>
            <button onClick={confirmDeleteRecord} className="btn btn-danger">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Удалить
            </button>
          </>
        }
      >
        <p className="text-gray-700">
          Вы уверены, что хотите удалить эту запись? Это действие нельзя отменить.
        </p>
      </Modal>
    </div>
  );
};

export default Databases;
