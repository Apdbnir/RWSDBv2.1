import { useState, useEffect, useRef } from 'react';

/**
 * CUA-compliant Update Record Dialog
 * Static form dialog for updating existing records
 * - Tab navigation between fields
 * - Enter = OK, Esc = Cancel
 * - No scrolling within form
 */
const UpdateRecordDialog = ({ isOpen, onClose, onConfirm, tableName, columns, record }) => {
  const [formData, setFormData] = useState({});
  const firstInputRef = useRef(null);

  useEffect(() => {
    if (record) {
      setFormData(record);
    }
  }, [record]);

  useEffect(() => {
    if (isOpen && firstInputRef.current) {
      firstInputRef.current.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;

      if (e.key === 'Escape') {
        e.preventDefault();
        onClose();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        onConfirm(formData);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, formData, onClose, onConfirm]);

  if (!isOpen) return null;

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const idColumn = columns.find(col => col.includes('id')) || columns[0];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div 
        className="bg-white rounded-lg shadow-xl w-full max-w-2xl"
        role="dialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-300 bg-gray-50">
          <h2 id="dialog-title" className="text-lg font-semibold text-gray-800">
            Update Record - {tableName}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-xl leading-none px-2"
            aria-label="Close dialog"
          >
            ×
          </button>
        </div>

        {/* Body - Form Fields */}
        <div className="p-6">
          <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded">
            <p className="text-sm text-blue-800">
              <strong>ID:</strong> {record?.[idColumn] || 'N/A'}
            </p>
          </div>
          <div className="space-y-4">
            {columns.filter(col => col !== 'created_at' && col !== 'updated_at' && col !== idColumn).map((col, index) => (
              <div key={col} className="flex items-center">
                <label 
                  htmlFor={`field-${col}`}
                  className="w-40 text-sm font-medium text-gray-700 flex-shrink-0"
                >
                  {col}:
                </label>
                <input
                  ref={index === 0 ? firstInputRef : null}
                  id={`field-${col}`}
                  type="text"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-sm"
                  value={formData[col] !== undefined && formData[col] !== null ? String(formData[col]) : ''}
                  onChange={(e) => handleChange(col, e.target.value)}
                  tabIndex={index + 1}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Footer - Action Buttons */}
        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-300 bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-white border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors text-sm font-medium min-w-[100px]"
            tabIndex={100}
          >
            Cancel
          </button>
          <button
            onClick={() => onConfirm(formData)}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm font-medium min-w-[100px]"
            tabIndex={101}
          >
            OK
          </button>
        </div>
      </div>
    </div>
  );
};

export default UpdateRecordDialog;
