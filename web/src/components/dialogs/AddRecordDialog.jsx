import { useState, useEffect, useRef } from 'react';
import { validateForm, getFieldPlaceholder, getFieldLabel } from '../../utils/validation';

/**
 * CUA-compliant Add Record Dialog with real-time validation
 * - Tab navigation between fields
 * - Enter = OK, Esc = Cancel
 * - Real-time validation feedback
 */
const AddRecordDialog = ({ isOpen, onClose, onConfirm, tableName, columns }) => {
  const [formData, setFormData] = useState({});
  const [validationErrors, setValidationErrors] = useState({});
  const [touchedFields, setTouchedFields] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const firstInputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setFormData({});
      setValidationErrors({});
      setTouchedFields({});
      setIsLoading(!columns || columns.length === 0);
    }
  }, [isOpen, columns]);

  useEffect(() => {
    if (isOpen && !isLoading && firstInputRef.current) {
      setTimeout(() => firstInputRef.current?.focus(), 100);
    }
  }, [isOpen, isLoading]);

  // Real-time validation
  useEffect(() => {
    if (isOpen && !isLoading) {
      const { errors } = validateForm(tableName, formData);
      setValidationErrors(errors);
    }
  }, [formData, tableName, isOpen, isLoading]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen || isLoading) return;

      if (e.key === 'Escape') {
        e.preventDefault();
        onClose();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        // Only submit if no validation errors
        if (Object.keys(validationErrors).length === 0) {
          onConfirm(formData);
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, isLoading, formData, validationErrors, onClose, onConfirm]);

  if (!isOpen) return null;

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleBlur = (field) => {
    setTouchedFields(prev => ({ ...prev, [field]: true }));
  };

  const formColumns = columns ? columns.filter(col => col !== 'created_at' && col !== 'updated_at') : [];
  
  // Check if form is valid (all touched fields have no errors)
  const hasErrors = Object.keys(validationErrors).length > 0;
  const isFormValid = !hasErrors && formColumns.every(col => formData[col] !== undefined && formData[col] !== '');

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
            Дадаць запіс - {tableName}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-xl leading-none px-2"
            aria-label="Close dialog"
          >
            ×
          </button>
        </div>

        {/* Body - Form Fields with validation */}
        <div className="p-6 max-h-[60vh] overflow-y-auto">
          {isLoading || formColumns.length === 0 ? (
            <div className="flex items-center justify-center py-12">
              <svg className="animate-spin h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              <span className="ml-3 text-gray-600">Загрузка палёў...</span>
            </div>
          ) : (
            <div className="space-y-4">
              {formColumns.map((col, index) => {
                const hasError = touchedFields[col] && validationErrors[col];
                const isValid = touchedFields[col] && !validationErrors[col] && formData[col];
                
                return (
                  <div key={col}>
                    <label
                      htmlFor={`field-${col}`}
                      className="block text-sm font-medium text-gray-700 mb-1"
                    >
                      {getFieldLabel(col)}
                    </label>
                    <input
                      ref={index === 0 ? firstInputRef : null}
                      id={`field-${col}`}
                      type="text"
                      className={`w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-sm ${
                        hasError
                          ? 'border-red-500 focus:ring-red-500'
                          : isValid
                          ? 'border-green-500 focus:ring-green-500'
                          : 'border-gray-300'
                      }`}
                      value={formData[col] || ''}
                      onChange={(e) => handleChange(col, e.target.value)}
                      onBlur={() => handleBlur(col)}
                      tabIndex={index + 1}
                      placeholder={getFieldPlaceholder(tableName, col)}
                    />
                    {/* Real-time validation feedback */}
                    {touchedFields[col] && (
                      <div className="mt-1 text-xs">
                        {isValid ? (
                          <p className="text-green-600 flex items-center gap-1">
                            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            Правільна
                          </p>
                        ) : hasError ? (
                          <p className="text-red-600 flex items-center gap-1">
                            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                            {validationErrors[col]}
                          </p>
                        ) : null}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer - Action Buttons */}
        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-300 bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-white border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors text-sm font-medium min-w-[100px]"
            tabIndex={isLoading ? -1 : formColumns.length + 1}
            disabled={isLoading}
          >
            Адмена
          </button>
          <button
            onClick={() => onConfirm(formData)}
            className={`px-6 py-2 rounded transition-colors text-sm font-medium min-w-[100px] ${
              isFormValid && !hasErrors && !isLoading && formColumns.length > 0
                ? 'bg-blue-600 text-white hover:bg-blue-700'
                : 'bg-gray-400 text-gray-200 cursor-not-allowed'
            }`}
            tabIndex={isLoading ? -1 : formColumns.length + 2}
            disabled={!isFormValid || hasErrors || isLoading || formColumns.length === 0}
          >
            ОК
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddRecordDialog;
