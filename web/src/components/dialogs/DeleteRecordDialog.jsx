import { useState, useEffect, useRef } from 'react';

/**
 * CUA-compliant Delete Record Dialog
 * Static dialog for confirming record deletion
 * - Enter = OK (confirm), Esc = Cancel
 */
const DeleteRecordDialog = ({ isOpen, onClose, onConfirm, tableName, recordId }) => {
  const [inputId, setInputId] = useState('');
  const inputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setInputId('');
      setTimeout(() => inputRef.current?.focus(), 100);
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
        if (inputId === String(recordId)) {
          onConfirm();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, inputId, recordId, onClose, onConfirm]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div 
        className="bg-white rounded-lg shadow-xl w-full max-w-md"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
        aria-describedby="dialog-description"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-300 bg-red-50">
          <h2 id="dialog-title" className="text-lg font-semibold text-red-800 flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Delete Record
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-xl leading-none px-2"
            aria-label="Close dialog"
          >
            ×
          </button>
        </div>

        {/* Body */}
        <div className="p-6">
          <p id="dialog-description" className="text-gray-700 mb-4">
            Are you sure you want to delete record <strong>ID={recordId}</strong> from table <strong>{tableName}</strong>?
          </p>
          <p className="text-sm text-red-600 mb-4">
            This action cannot be undone. Please enter the record ID to confirm:
          </p>
          <div className="flex items-center gap-3">
            <label htmlFor="delete-id-input" className="text-sm font-medium text-gray-700">
              Record ID:
            </label>
            <input
              ref={inputRef}
              id="delete-id-input"
              type="text"
              className="flex-1 px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none text-sm"
              value={inputId}
              onChange={(e) => setInputId(e.target.value)}
              placeholder="Enter record ID"
            />
          </div>
        </div>

        {/* Footer - Action Buttons */}
        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-300 bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-white border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors text-sm font-medium min-w-[100px]"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={inputId !== String(recordId)}
            className="px-6 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors text-sm font-medium min-w-[100px] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteRecordDialog;
