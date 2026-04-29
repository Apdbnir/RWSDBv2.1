import { useEffect } from 'react';

/**
 * CUA-compliant Exit Confirmation Dialog
 * Static dialog for confirming application exit
 * - Enter = Yes (exit), Esc = No (cancel)
 */
const ExitConfirmDialog = ({ isOpen, onClose, onConfirm }) => {
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
        className="bg-white rounded-lg shadow-xl w-full max-w-sm"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
        aria-describedby="dialog-description"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-300 bg-orange-50">
          <h2 id="dialog-title" className="text-lg font-semibold text-orange-800 flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Выхад з сістэмы
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
          <p id="dialog-description" className="text-gray-700">
            Вы ўпэўнены, што хочаце выйсці з сістэмы?
          </p>
        </div>

        {/* Footer - Action Buttons */}
        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-300 bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-white border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors text-sm font-medium min-w-[100px]"
          >
            Не
          </button>
          <button
            onClick={onConfirm}
            className="px-6 py-2 bg-orange-600 text-white rounded hover:bg-orange-700 transition-colors text-sm font-medium min-w-[100px]"
          >
            Так, выйсці
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExitConfirmDialog;
