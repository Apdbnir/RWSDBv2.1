# This file is maintained for backward compatibility
# The main functionality has been refactored into separate modules
# See the new structure:
# - database/manager.py - Core database operations
# - ui/mainwindow.py - Main UI components
# - utils/translations.py - Translation functionality
# - utils/backup/backup_manager.py - Backup functionality
# - utils/query_history.py - Query history management
# - app/main.py - Main application entry point

# This file can be used to import the main classes if needed elsewhere
from database.manager import DatabaseManager, TableModel
from ui.mainwindow import DatabaseApp

__all__ = ['DatabaseManager', 'TableModel', 'DatabaseApp']