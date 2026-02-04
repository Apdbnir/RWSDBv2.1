"""
Constants module for the Database Management System.

This module contains all the constants used throughout the application
to improve maintainability and consistency.
"""

# Application constants
APP_NAME = "Database Management System"
APP_VERSION = "2.0"
DEFAULT_ADMIN_PASSWORD = "4444"

# Database constants
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = 5432
DEFAULT_DB_NAME = "railway_station"
DEFAULT_DB_USER = "postgres"

# Security constants
DEFAULT_ADMIN_PASSWORD_PLAIN = "4444"

# UI constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Color constants for data type highlighting
COLOR_NUMERIC_BG = "#d5f4e6"  # Light green background
COLOR_NUMERIC_FG = "#27ae60"  # Green text
COLOR_DATE_BG = "#fdf2e9"     # Light orange background
COLOR_DATE_FG = "#e67e22"     # Orange text
COLOR_BOOLEAN_BG = "#e8f6f3"  # Light teal background
COLOR_BOOLEAN_FG = "#16a085"  # Teal text
COLOR_TEXT_BG = "#e8f4fd"     # Light blue background
COLOR_TEXT_FG = "#2980b9"     # Blue text

# UI element sizes
TABLE_ROW_HEIGHT = 30
TABLE_COLUMN_MIN_WIDTH = 100

# Query execution constants
MAX_QUERY_PREVIEW_LENGTH = 100
MAX_PARAM_PREVIEW_LENGTH = 50

# File paths
CONFIG_FILE_PATH = "config.json"
LOG_DIR = "logs"
BACKUP_DIR = "backups"

# Message constants
MSG_READY = "Ready"
MSG_CONNECTED_TO_DB = "Connected to {database}"
MSG_TABLE_CREATED = "Table '{table}' created successfully"
MSG_TABLE_DELETED = "Table '{table}' deleted successfully"
MSG_COLUMN_ADDED = "Column '{column}' added to table '{table}'"
MSG_COLUMN_DELETED = "Column '{column}' deleted from table '{table}'"
MSG_ROW_ADDED = "New row added to table '{table}'"
MSG_ROW_DELETED = "Row deleted from table '{table}'"
MSG_QUERY_EXECUTED = "Query executed successfully"
MSG_QUERY_EXECUTED_ROWS = "Query executed successfully. {count} rows returned."
MSG_TRANSACTION_STARTED = "Transaction started successfully"
MSG_TRANSACTION_COMMITTED = "Transaction committed successfully"
MSG_TRANSACTION_ROLLED_BACK = "Transaction rolled back successfully"
MSG_BACKUP_CREATED = "Backup created successfully: {path}"
MSG_DATABASE_RESTORED = "Database restored successfully: {path}"
MSG_TABLE_EXPORTED = "Table '{table}' exported to {path}"
MSG_QUERY_RESULTS_EXPORTED = "Query results exported to {path}"
MSG_PREDEFINED_QUERY_EXECUTED = "Predefined query executed successfully"
MSG_PREDEFINED_QUERY_EXECUTED_ROWS = "Predefined query executed successfully. {count} rows returned."

# Error messages
ERROR_NO_DB_CONNECTION = "Please connect to a database first."
ERROR_NO_TABLE_SELECTED = "Please select a table first."
ERROR_NO_ROW_SELECTED = "Please select a row to delete."
ERROR_INVALID_QUERY = "Please enter a query to execute."
ERROR_ACCESS_RESTRICTED = "You are in User Mode (Read-only). Data modification queries are not allowed."
ERROR_BACKUP_CREATION_FAILED = "Failed to create backup."
ERROR_RESTORE_FAILED = "Failed to restore backup."
ERROR_CONNECTION_FAILED = "Failed to connect to the database."
ERROR_QUERY_EXECUTION_FAILED = "Error executing query: {error}"

# Confirmation messages
CONFIRM_DELETE_TABLE = "Are you sure you want to delete table '{table_name}'?"
CONFIRM_DELETE_ROW = "Are you sure you want to delete row with {pk_column_name}={pk_value}?"
CONFIRM_COMMIT_TRANSACTION = "Are you sure you want to commit the current transaction? This will make all changes permanent."
CONFIRM_ROLLBACK_TRANSACTION = "Are you sure you want to rollback the current transaction? This will undo all changes made since the transaction began."
CONFIRM_EXIT_USER_MODE = "Are you sure you want to exit the application? (User Mode)"
CONFIRM_EXIT_ADMIN_MODE = "Are you sure you want to exit the application? (Administrator Mode)"
CONFIRM_UNCOMMITTED_TRANSACTION = "There is an uncommitted transaction. Do you want to commit before closing?"

# User modes
USER_MODE_ADMIN = "admin"
USER_MODE_USER = "user"
MSG_USER_MODE_READ_ONLY = "User mode: Read-only access"
MSG_ADMIN_MODE_FULL_ACCESS = "Administrator mode: Full access"

# Tab names
TAB_NAME_TABLE_VIEW = "table_view_tab"
TAB_NAME_SPECIAL_QUERIES = "special_queries_tab"
TAB_NAME_QUERY_EDITOR = "query_editor_tab"
TAB_NAME_QUERY_HISTORY = "query_history_tab"
TAB_NAME_ENTITY_OPERATIONS = "entity_operations_tab"
TAB_NAME_SELECT_QUERIES = "select_queries_tab"
TAB_NAME_JOIN_QUERIES = "join_queries_tab"
TAB_NAME_AGGREGATE_QUERIES = "aggregate_queries_tab"
TAB_NAME_SAVED_QUERIES = "saved_queries_tab"

# Button/object names for styling
BUTTON_NAME_ADD = "add"
BUTTON_NAME_DELETE = "delete"
BUTTON_NAME_EDIT = "edit"
BUTTON_NAME_REFRESH = "refresh"
BUTTON_NAME_SAVE = "save"
BUTTON_NAME_CANCEL = "cancel"
BUTTON_NAME_YES = "yes"
BUTTON_NAME_OK = "ok"
BUTTON_NAME_EXIT = "exit"
BUTTON_NAME_REMOVE = "remove"
BUTTON_NAME_APPLY = "apply"
BUTTON_NAME_VIEW = "view"
BUTTON_NAME_UPDATE = "update"
BUTTON_NAME_CHANGE = "change"
BUTTON_NAME_MODIFY = "modify"
BUTTON_NAME_PURPLE = "purple"
BUTTON_NAME_RED = "red"
BUTTON_NAME_ORANGE = "orange"

# SQL keywords for syntax highlighting
SQL_KEYWORDS = [
    'SELECT', 'FROM', 'WHERE', 'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT',
    'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER', 'TABLE',
    'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'CROSS',
    'UNION', 'INTERSECT', 'EXCEPT', 'DISTINCT', 'AS', 'AND', 'OR', 'NOT',
    'IN', 'EXISTS', 'BETWEEN', 'LIKE', 'IS', 'NULL', 'PRIMARY', 'KEY',
    'FOREIGN', 'REFERENCES', 'CONSTRAINT', 'CHECK', 'DEFAULT', 'UNIQUE',
    'INDEX', 'VIEW', 'TRIGGER', 'PROCEDURE', 'FUNCTION', 'BEGIN', 'END',
    'COMMIT', 'ROLLBACK', 'TRANSACTION', 'SAVEPOINT', 'GRANT', 'REVOKE'
]

# Data types
DATA_TYPE_NUMERIC = "numeric"
DATA_TYPE_TEXT = "text"
DATA_TYPE_DATE = "date"
DATA_TYPE_BOOLEAN = "boolean"