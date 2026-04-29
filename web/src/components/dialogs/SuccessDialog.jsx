import { useEffect } from 'react';

/**
 * CUA-compliant Success Notification Dialog
 * Static dialog for displaying operation results
 * - Enter or Esc to close
 */
const SuccessDialog = ({ isOpen, onClose, title, message, details = null }) => {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;

      if (e.key === 'Escape' || e.key === 'Enter') {
        e.preventDefault();
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div 
        className="bg-white rounded-lg shadow-xl w-full max-w-md"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-300 bg-green-50">
          <h2 id="dialog-title" className="text-lg font-semibold text-green-800 flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {title || 'Success'}
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
          <p className="text-gray-700 mb-3">{message}</p>
          {details && (
            <div className="bg-gray-50 border border-gray-200 rounded p-3">
              <p className="text-xs text-gray-600 font-mono break-all">{details}</p>
            </div>
          )}
        </div>

        {/* Footer - Action Button */}
        <div className="flex items-center justify-end px-6 py-4 border-t border-gray-300 bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors text-sm font-medium min-w-[100px]"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  );
};

export default SuccessDialog;
