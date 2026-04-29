import { useState, useEffect, useRef } from 'react';

/**
 * CUA-compliant Special Queries Dialog
 * Static dialog for selecting and executing predefined queries
 * - Arrow keys to navigate list
 * - Enter = Execute, Esc = Cancel
 */
const SpecialQueriesDialog = ({ isOpen, onClose, onExecute, queries }) => {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const listRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setSelectedIndex(0);
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
        if (queries[selectedIndex]) {
          onExecute(queries[selectedIndex].id);
        }
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(prev => Math.min(prev + 1, queries.length - 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(prev => Math.max(prev - 1, 0));
      } else if (e.key === 'Home') {
        e.preventDefault();
        setSelectedIndex(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        setSelectedIndex(queries.length - 1);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, selectedIndex, queries, onClose, onExecute]);

  useEffect(() => {
    if (isOpen && listRef.current) {
      const selectedElement = listRef.current.children[selectedIndex];
      if (selectedElement) {
        selectedElement.scrollIntoView({ block: 'nearest' });
      }
    }
  }, [selectedIndex, isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div 
        className="bg-white rounded-lg shadow-xl w-full max-w-lg"
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
            Special Queries
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-xl leading-none px-2"
            aria-label="Close dialog"
          >
            ×
          </button>
        </div>

        {/* Body - Query List */}
        <div className="p-6">
          <p className="text-sm text-gray-600 mb-3">
            Select a query to execute:
          </p>
          <div 
            ref={listRef}
            className="border border-gray-300 rounded max-h-80 overflow-y-auto"
            role="listbox"
            aria-label="Available queries"
          >
            {queries.map((query, index) => (
              <div
                key={query.id}
                onClick={() => setSelectedIndex(index)}
                onDoubleClick={() => onExecute(query.id)}
                className={`px-4 py-3 cursor-pointer border-b border-gray-100 last:border-b-0 flex items-center justify-between ${
                  index === selectedIndex 
                    ? 'bg-blue-600 text-white' 
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
                role="option"
                aria-selected={index === selectedIndex}
              >
                <div>
                  <p className="font-medium text-sm">{query.name}</p>
                  <p className={`text-xs mt-1 ${index === selectedIndex ? 'text-blue-100' : 'text-gray-500'}`}>
                    {query.description}
                  </p>
                </div>
                <svg className="w-4 h-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            ))}
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
            onClick={() => onExecute(queries[selectedIndex]?.id)}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm font-medium min-w-[100px]"
          >
            Execute
          </button>
        </div>
      </div>
    </div>
  );
};

export default SpecialQueriesDialog;
