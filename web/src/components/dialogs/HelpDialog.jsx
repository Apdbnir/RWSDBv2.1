import { useEffect, useRef } from 'react';

/**
 * CUA-compliant Help Dialog
 * Displays keyboard shortcuts and usage information
 */
const HelpDialog = ({ isOpen, onClose }) => {
  const closeButtonRef = useRef(null);

  useEffect(() => {
    if (isOpen && closeButtonRef.current) {
      setTimeout(() => closeButtonRef.current?.focus(), 100);
    }
  }, [isOpen]);

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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div
        className="bg-white rounded-lg shadow-xl w-full max-w-4xl my-8"
        role="dialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-300 bg-blue-50">
          <h2 id="dialog-title" className="text-xl font-semibold text-gray-800 flex items-center gap-2">
            <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Help - Keyboard Shortcuts
          </h2>
          <button
            ref={closeButtonRef}
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-xl leading-none px-2"
            aria-label="Close dialog"
            tabIndex={0}
          >
            ×
          </button>
        </div>

        {/* Body - Help Content */}
        <div className="p-6 max-h-[70vh] overflow-y-auto">
          <div className="space-y-6">
            {/* Menu Access */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="w-6 h-6 bg-blue-100 text-blue-700 rounded flex items-center justify-center text-sm font-bold">1</span>
                Menu Access
              </h3>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Open File menu</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">F</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Open Tables menu</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">T</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Open Operations menu</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">O</kbd>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Open Export menu</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">X</kbd>
                </div>
              </div>
            </div>

            {/* Table Selection (T then...) */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="w-6 h-6 bg-blue-100 text-blue-700 rounded flex items-center justify-center text-sm font-bold">2</span>
                Table Selection (press T then number)
              </h3>
              <div className="bg-gray-50 rounded-lg p-4 grid grid-cols-2 gap-2">
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Schedule</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">1</kbd>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Train</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">2</kbd>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Platform</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">3</kbd>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Passenger</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">4</kbd>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Ticket</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">5</kbd>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Employee</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">6</kbd>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Service</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">7</kbd>
                </div>
              </div>
            </div>

            {/* Operations (O then...) */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="w-6 h-6 bg-blue-100 text-blue-700 rounded flex items-center justify-center text-sm font-bold">3</span>
                Operations (press O then letter)
              </h3>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">View (refresh table)</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">V</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Add record</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">A</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Update record</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">U</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Delete record</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">D</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Special Queries</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">Q</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Custom Query</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">C</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Save Query result</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">S</kbd>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Backup (superuser only)</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">B</kbd>
                </div>
              </div>
            </div>

            {/* Export (X then...) */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="w-6 h-6 bg-blue-100 text-blue-700 rounded flex items-center justify-center text-sm font-bold">4</span>
                Export (press X then letter)
              </h3>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Export to JSON</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">J</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Export to CSV</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">C</kbd>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Export to Excel</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">E</kbd>
                </div>
              </div>
            </div>

            {/* Direct Actions */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="w-6 h-6 bg-blue-100 text-blue-700 rounded flex items-center justify-center text-sm font-bold">5</span>
                Direct Actions (no menu)
              </h3>
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Add / Delete / Update / Refresh</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">A / D / U / V</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Navigate rows (up/down)</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">↑ / ↓</kbd>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-200">
                  <span className="text-gray-700">Select row</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">Space / Enter</kbd>
                </div>
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Exit application</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">E</kbd>
                </div>
              </div>
            </div>

            {/* File (F then...) */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <span className="w-6 h-6 bg-blue-100 text-blue-700 rounded flex items-center justify-center text-sm font-bold">6</span>
                File Menu (press F then)
              </h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-700">Exit application</span>
                  <kbd className="px-3 py-1 bg-gray-200 rounded text-sm font-mono">E</kbd>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end px-6 py-4 border-t border-gray-300 bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm font-medium min-w-[100px]"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default HelpDialog;
