import { useEffect } from 'react';

/**
 * Custom hook for CUA-compliant keyboard shortcuts
 * Implements Common User Access standard hotkeys
 *
 * Menu access: F for File, T for Tables, O for Operations, X for Export
 * All shortcuts use preventDefault() to block browser default actions
 */
const useKeyboardShortcuts = ({
  onAdd,
  onView,
  onUpdate,
  onDelete,
  onQueries,
  onSaveQuery,
  onBackup,
  onExit,
  onExport,
  onExportJSON,
  onExportCSV,
  onExportExcel,
  activeTable,
  hasQueryResult,
  isSuperUser,
  onTableSelect,
  onHelp
}) => {
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ignore shortcuts when typing in input fields/dialogs
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
        return;
      }

      const key = e.key.toLowerCase();

      // H or ? - Help (must be first, before any other checks)
      if (key === 'h' || key === '?') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (onHelp) onHelp();
        return false;
      }

      // ===== MENU ACCESS =====
      // F - Open File menu
      if (key === 'f') {
        e.preventDefault();
        e.stopImmediatePropagation();
        // Signal to open File menu
        if (window.onOpenFileMenu) window.onOpenFileMenu();
        return false;
      }

      // T - Open Tables menu (with number for specific table)
      if (key === 't') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (window.onOpenTablesMenu) window.onOpenTablesMenu();
        return false;
      }

      // O - Open Operations menu
      if (key === 'o') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (window.onOpenOperationsMenu) window.onOpenOperationsMenu();
        return false;
      }

      // X - Open Export menu
      if (key === 'x') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (window.onOpenExportMenu) window.onOpenExportMenu();
        return false;
      }

      // ===== FILE MENU (F then...) =====
      // E - Exit (after F)
      if (key === 'e' && window.menuContext === 'file') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (onExit) onExit();
        window.menuContext = null;
        return false;
      }

      // ===== TABLES MENU (T then...) =====
      // Numbers 1-7 for tables (after T)
      if (window.menuContext === 'tables') {
        const tableMap = {
          '1': 'schedule',
          '2': 'train',
          '3': 'platform',
          '4': 'passenger',
          '5': 'ticket',
          '6': 'employee',
          '7': 'service'
        };
        if (tableMap[key] && onTableSelect) {
          e.preventDefault();
          e.stopImmediatePropagation();
          onTableSelect(tableMap[key]);
          window.menuContext = null;
          return false;
        }
      }

      // ===== OPERATIONS MENU (O then...) =====
      if (window.menuContext === 'operations') {
        // V - View
        if (key === 'v') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (onView) onView();
          window.menuContext = null;
          return false;
        }
        // A - Add
        if (key === 'a') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (onAdd) onAdd();
          window.menuContext = null;
          return false;
        }
        // U - Update
        if (key === 'u') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (onUpdate) onUpdate();
          window.menuContext = null;
          return false;
        }
        // D - Delete
        if (key === 'd') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (onDelete) onDelete();
          window.menuContext = null;
          return false;
        }
        // Q - Special Queries
        if (key === 'q') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (onQueries) onQueries();
          window.menuContext = null;
          return false;
        }
        // C - Custom Query
        if (key === 'c') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (window.onOpenCustomQuery) window.onOpenCustomQuery();
          window.menuContext = null;
          return false;
        }
        // S - Save Query
        if (key === 's') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (hasQueryResult && onSaveQuery) onSaveQuery();
          window.menuContext = null;
          return false;
        }
        // B - Backup
        if (key === 'b') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (isSuperUser && onBackup) onBackup();
          window.menuContext = null;
          return false;
        }
      }

      // ===== EXPORT MENU (X then...) =====
      if (window.menuContext === 'export') {
        // J - Export to JSON
        if (key === 'j') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (onExportJSON) onExportJSON('json');
          window.menuContext = null;
          return false;
        }
        // C - Export to CSV
        if (key === 'c') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (onExportCSV) onExportCSV('csv');
          window.menuContext = null;
          return false;
        }
        // E - Export to Excel
        if (key === 'e') {
          e.preventDefault();
          e.stopImmediatePropagation();
          if (onExportExcel) onExportExcel('excel');
          window.menuContext = null;
          return false;
        }
      }

      // ===== DIRECT ACTION SHORTCUTS (no menu) =====
      // A - Add record
      if (key === 'a') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (activeTable && onAdd) {
          onAdd();
        }
        return false;
      }

      // V - View table (refresh)
      if (key === 'v') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (activeTable && onView) {
          onView();
        }
        return false;
      }

      // D - Delete record
      if (key === 'd') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (activeTable && onDelete) {
          onDelete();
        }
        return false;
      }

      // U - Update record
      if (key === 'u') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (activeTable && onUpdate) {
          onUpdate();
        }
        return false;
      }

      // Q - Execute special query
      if (key === 'q') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (onQueries) {
          onQueries();
        }
        return false;
      }

      // S - Save query result
      if (key === 's') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (hasQueryResult && onSaveQuery) {
          onSaveQuery();
        }
        return false;
      }

      // B - Create backup (superuser only)
      if (key === 'b') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (isSuperUser && onBackup) {
          onBackup();
        }
        return false;
      }

      // E - Exit application
      if (key === 'e') {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (onExit) {
          onExit();
        }
        return false;
      }
    };

    // Use capture phase to intercept before browser
    document.addEventListener('keydown', handleKeyDown, true);
    return () => document.removeEventListener('keydown', handleKeyDown, true);
  }, [
    onAdd, onView, onUpdate, onDelete, onQueries, onSaveQuery, onBackup, onExit,
    onExport, onExportJSON, onExportCSV, onExportExcel, onTableSelect,
    activeTable, hasQueryResult, isSuperUser
  ]);
};

export default useKeyboardShortcuts;
