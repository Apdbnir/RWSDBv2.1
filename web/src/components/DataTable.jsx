import { useEffect } from 'react';

const DataTable = ({ 
  columns, 
  data, 
  onRowClick, 
  onEdit, 
  onDelete, 
  canEdit = true, 
  canDelete = true, 
  selectedRows = [], 
  onRowSelect,
  focusedRowIndex,
  onFocusedRowChange
}) => {
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
        <p>Нет данных для отображения</p>
      </div>
    );
  }

  const getRowId = (row, index) => {
    // Try to find a unique identifier in the row
    const id = row.id || 
               row.passenger_number || 
               row.ticket_number || 
               row.schedule_number || 
               row.train_number || 
               row.platform_number || 
               row.employee_number || 
               row.service_number;
    
    if (id !== undefined && id !== null) {
      return id.toString();
    }
    
    // Fallback to index if no ID found
    return `row-${index}`;
  };

  const isSelected = (row, index) => {
    const rowId = getRowId(row, index);
    return selectedRows.some(r => {
      const selectedId = getRowId(r, -1);
      return selectedId === rowId;
    });
  };

  const handleRowClick = (e, row, index) => {
    if (onRowSelect) {
      e.stopPropagation();
      onRowSelect(row, e.ctrlKey || e.metaKey);
    }
    onRowClick?.(row);
  };

  // Handle keyboard navigation for table
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Only handle if we're in table context (not in input/dialog)
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
        return;
      }

      if (onFocusedRowChange && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
        e.preventDefault();
        e.stopImmediatePropagation();
        
        if (e.key === 'ArrowDown') {
          onFocusedRowChange(prev => Math.min(prev + 1, data.length - 1));
        } else if (e.key === 'ArrowUp') {
          onFocusedRowChange(prev => Math.max(prev - 1, 0));
        }
        return false;
      }

      // Space or Enter to select/toggle row
      if (onRowSelect && (e.key === ' ' || e.key === 'Enter')) {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (focusedRowIndex !== null && focusedRowIndex < data.length) {
          onRowSelect(data[focusedRowIndex], e.ctrlKey || e.metaKey);
        }
        return false;
      }
    };

    document.addEventListener('keydown', handleKeyDown, true);
    return () => document.removeEventListener('keydown', handleKeyDown, true);
  }, [data, focusedRowIndex, onRowSelect, onFocusedRowChange]);

  // Scroll focused row into view
  useEffect(() => {
    if (focusedRowIndex !== null) {
      const rowElement = document.getElementById(`row-${focusedRowIndex}`);
      if (rowElement) {
        rowElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }
  }, [focusedRowIndex]);

  return (
    <div className="overflow-x-auto">
      <table className="data-table w-full">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key} className="px-4 py-3 text-left font-semibold text-gray-700 bg-gray-50">
                {column.label}
              </th>
            ))}
            {(canEdit || canDelete) && (
              <th className="text-right px-4 py-3 font-semibold text-gray-700 bg-gray-50">Действия</th>
            )}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => {
            const rowIsSelected = isSelected(row, rowIndex);
            const isFocused = focusedRowIndex === rowIndex;
            return (
              <tr
                id={`row-${rowIndex}`}
                key={getRowId(row, rowIndex)}
                onClick={(e) => handleRowClick(e, row, rowIndex)}
                className={`
                  transition-colors cursor-pointer
                  ${rowIsSelected ? 'bg-blue-200 hover:bg-blue-300' : 'hover:bg-gray-50'}
                  ${isFocused ? 'ring-2 ring-blue-500 ring-inset' : ''}
                `}
              >
                {columns.map((column) => (
                  <td key={column.key} className="px-4 py-3 border-b border-gray-100">
                    {column.render ? column.render(row[column.key], row) : row[column.key]}
                  </td>
                ))}
                {(canEdit || canDelete) && (
                  <td className="text-right px-4 py-3 border-b border-gray-100">
                    <div className="flex items-center justify-end gap-2">
                      {canEdit && onEdit && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onEdit(row);
                          }}
                          className="btn btn-sm btn-primary"
                          title="Редактировать"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                      )}
                      {canDelete && onDelete && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onDelete(row);
                          }}
                          className="btn btn-sm btn-danger"
                          title="Удалить"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      )}
                    </div>
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;
