import { useState, useEffect, useRef } from 'react';

/**
 * CUA-compliant Backup Dialog
 * Static dialog for creating database backup
 * Requires superuser password confirmation
 * - Enter = OK, Esc = Cancel
 */
const BackupDialog = ({ isOpen, onClose, onConfirm }) => {
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const passwordInputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setPassword('');
      setTimeout(() => passwordInputRef.current?.focus(), 100);
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
        if (password.trim()) {
          onConfirm(password);
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, password, onClose, onConfirm]);

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
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-300 bg-purple-50">
          <h2 id="dialog-title" className="text-lg font-semibold text-purple-800 flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
            </svg>
            Create Database Backup
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
            Creating a backup requires superuser privileges.
          </p>
          <div className="bg-yellow-50 border border-yellow-200 rounded p-3 mb-4">
            <p className="text-sm text-yellow-800">
              <strong>⚠️ Important:</strong> This operation can only be performed by a superuser.
            </p>
          </div>
          <div className="flex items-center gap-3 mb-3">
            <label htmlFor="backup-password" className="text-sm font-medium text-gray-700 w-28">
              Password:
            </label>
            <div className="flex-1 relative">
              <input
                ref={passwordInputRef}
                id="backup-password"
                type={showPassword ? 'text' : 'password'}
                className="w-full px-3 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none text-sm"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter superuser password"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 text-xs"
              >
                {showPassword ? '👁' : '👁‍🗨'}
              </button>
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
            onClick={() => onConfirm(password)}
            disabled={!password.trim()}
            className="px-6 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors text-sm font-medium min-w-[100px] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Create Backup
          </button>
        </div>
      </div>
    </div>
  );
};

export default BackupDialog;
