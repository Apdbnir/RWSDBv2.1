import { useState, useEffect } from 'react';
import api from '../../services/api';

/**
 * CUA-compliant Custom Query Dialog
 * Allows users to enter and execute custom SQL queries
 */
const CustomQueryDialog = ({ isOpen, onClose, onExecute }) => {
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      setQuery('');
      setError('');
    }
  }, [isOpen]);

  const handleSubmit = async () => {
    if (!query.trim()) {
      setError('Please enter a SQL query');
      return;
    }

    // Basic SQL injection protection - only allow SELECT queries
    const trimmedQuery = query.trim();
    if (!trimmedQuery.toUpperCase().startsWith('SELECT')) {
      setError('Only SELECT queries are allowed for security reasons');
      return;
    }

    try {
      await onExecute(query);
      setQuery('');
      setError('');
    } catch (err) {
      setError(err.message || 'Query execution failed');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      e.preventDefault();
      onClose();
    } else if (e.key === 'Enter' && e.ctrlKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  if (!isOpen) return null;

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
          <h2 id="dialog-title" className="text-lg font-semibold text-gray-800 flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Custom SQL Query
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
          <label htmlFor="sql-query" className="block text-sm font-medium text-gray-700 mb-2">
            Enter your SQL query (SELECT only):
          </label>
          <textarea
            id="sql-query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            className="w-full h-40 p-3 border border-gray-300 rounded font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="SELECT * FROM table_name WHERE condition..."
            autoFocus
          />
          {error && (
            <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded">
              <p className="text-sm text-red-700 flex items-center gap-2">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                {error}
              </p>
            </div>
          )}
          <p className="mt-2 text-xs text-gray-500">
            Tip: Press Ctrl+Enter to execute, Esc to cancel
          </p>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-300 bg-gray-50">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-white border border-gray-300 text-gray-700 rounded hover:bg-gray-50 transition-colors text-sm font-medium min-w-[100px]"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm font-medium min-w-[100px]"
          >
            Execute
          </button>
        </div>
      </div>
    </div>
  );
};

export default CustomQueryDialog;
