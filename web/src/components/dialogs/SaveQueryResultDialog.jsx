import { useEffect } from 'react';

/**
 * CUA-compliant Save Query Result Dialog
 * Static dialog for saving query results to file
 * - Enter = OK, Esc = Cancel
 */
const SaveQueryResultDialog = ({ isOpen, onClose, onConfirm, tableName, recordCount }) => {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;

      if (e.key === 'Escape') {
        e.preventDefault();
        onClose();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        onConfirm();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose, onConfirm]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div 
        className="bg-white rounded-lg shadow-xl w-full max-w-md"
        role="dialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-300 bg-green-50">
          <h2 id="dialog-title" className="text-lg font-semibold text-green-800 flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
            </svg>
            Save Query Result
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
          <p className="text-gray-700 mb-4">
            Save the query results to a file on the server.
          </p>
          <div className="bg-gray-50 border border-gray-200 rounded p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Table:</span>
              <span className="font-medium text-gray-800">{tableName}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Records:</span>
              <span className="font-medium text-gray-800">{recordCount}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Format:</span>
              <span className="font-medium text-gray-800">Excel (.xlsx)</span>
            </div>
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
            className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors text-sm font-medium min-w-[100px]"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default SaveQueryResultDialog;
