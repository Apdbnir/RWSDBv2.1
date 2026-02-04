"""
Database Manager Module

This module provides a comprehensive database management system that supports both PostgreSQL and future database types.
It includes functionality for connection management, query execution, transaction handling, and metadata retrieval.

The DatabaseManager class handles all database operations with proper error handling, logging, and transaction support.
"""

import sys
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
                             QPushButton, QComboBox, QLineEdit, QLabel, QGroupBox,
                             QFormLayout, QScrollArea, QSplitter, QFrame, QFileDialog,
                             QMessageBox, QDialog, QInputDialog, QCheckBox, QSpinBox, QTextEdit)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QAction, QKeySequence
import openpyxl
from openpyxl.styles import Font, PatternFill
import psycopg2
from psycopg2 import sql
from utils.db_logging import db_logger
import logging


class DatabaseManager:
    """
    A database manager class that handles connections, queries, and transactions for PostgreSQL databases.

    Attributes:
        db_type (str): The type of database ('postgresql')
        connection_params (dict): Parameters for database connection
        connection: Database connection object
        cursor: Database cursor object
        in_transaction (bool): Flag indicating if a transaction is active
        transaction_stack (list): Stack for nested transaction management
        logger: Logger instance for the database manager
    """
    def __init__(self, db_type='postgresql', connection_params=None):
        """
        Initialize the DatabaseManager with connection parameters.

        Args:
            db_type (str): Type of database to connect to (currently only supports 'postgresql')
            connection_params (dict, optional): Connection parameters for the database
        """
        self.db_type = db_type
        self.connection_params = connection_params or {}
        self.connection = None
        self.cursor = None
        self.in_transaction = False
        self.transaction_stack = []
        self.logger = logging.getLogger(__name__)
        self.connect()

    def connect(self):
        """
        Establish a connection to the database using the provided connection parameters.

        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            self.logger.info(f"Attempting to connect to {self.db_type} database: {self.connection_params.get('database', 'unknown')}")
            if self.db_type == 'postgresql':
                self.connection = psycopg2.connect(**self.connection_params)
                self.cursor = self.connection.cursor()

                # Test the connection with a simple query
                self.cursor.execute("SELECT 1")
                result = self.cursor.fetchone()
                if result:
                    self.logger.info("PostgreSQL connection successful!")
                else:
                    self.logger.error("PostgreSQL connection test failed")
                    return False
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")

            # Log successful connection
            db_logger.log_connection_attempt(self.db_type, self.connection_params, success=True)
            return True
        except psycopg2.Error as e:
            error_msg = f"PostgreSQL error: {str(e)}"
            self.logger.error(error_msg)
            db_logger.log_connection_attempt(self.db_type, self.connection_params, success=False, error_msg=error_msg)
            return False
        except Exception as e:
            error_msg = f"Unexpected error during connection: {str(e)}"
            self.logger.error(error_msg)
            db_logger.log_connection_attempt(self.db_type, self.connection_params, success=False, error_msg=error_msg)
            return False

    def is_connected(self):
        """
        Check if the database connection is still active.

        Returns:
            bool: True if connection is active, False otherwise
        """
        if not self.connection:
            return False

        try:
            # Test the connection with a simple query
            self.cursor.execute("SELECT 1")
            self.connection.commit()  # Commit any pending transaction
            return True
        except:
            return False

    def reconnect(self):
        """
        Attempt to reconnect to the database.

        Returns:
            bool: True if reconnection is successful, False otherwise
        """
        self.close()  # Close existing connection if any
        return self.connect()

    def execute_query(self, query, params=None):
        """
        Execute a SQL query against the database.

        Args:
            query (str): The SQL query to execute
            params (tuple or list, optional): Parameters to bind to the query

        Returns:
            list or None: Query results for SELECT queries, None for others

        Raises:
            psycopg2.Error: If a PostgreSQL-specific error occurs
            Exception: If any other error occurs
        """
        # Check if connection is still alive, reconnect if necessary
        if not self.is_connected():
            self.logger.warning("Connection lost, attempting to reconnect...")
            if not self.reconnect():
                raise Exception("Unable to reconnect to database")

        try:
            self.logger.debug(f"Executing query: {query[:100]}...")  # First 100 characters of the query

            # Validate inputs
            if not query or not isinstance(query, str):
                raise ValueError("Query must be a non-empty string")

            # Sanitize query to prevent SQL injection
            if not self._is_safe_query(query):
                raise ValueError("Query contains unsafe elements")

            # PostgreSQL uses %s for psycopg2 parameter placeholders
            processed_query = query
            processed_params = params

            if self.db_type == 'postgresql' and params:
                # Count the number of ? placeholders
                param_count = query.count('?')
                if param_count > 0:
                    # Replace ? with %s for PostgreSQL/psycopg2
                    processed_query = query.replace('?', '%s')

            if processed_params is not None:
                self.logger.debug(f"With parameters: {[str(p)[:50] + '...' if len(str(p)) > 50 else str(p) for p in processed_params]}")
                self.cursor.execute(processed_query, processed_params)
            else:
                self.cursor.execute(processed_query)

            if query.strip().upper().startswith('SELECT'):
                result = self.cursor.fetchall()
                self.logger.info(f"SELECT query returned {len(result) if result else 0} rows")
                db_logger.log_query_execution(query, params, success=True, row_count=len(result) if result else 0)
                return result
            else:
                # Only commit if not in an active transaction
                if not self.in_transaction:
                    self.connection.commit()
                self.logger.info("Non-SELECT query executed successfully")
                db_logger.log_query_execution(query, params, success=True)
                return None
        except psycopg2.OperationalError as e:
            # Handle connection-related errors by attempting to reconnect
            error_msg = f"PostgreSQL operational error during query execution: {str(e)}"
            self.logger.error(error_msg)

            # Try to reconnect and retry the query once
            if "connection" in str(e).lower() or "server closed" in str(e).lower():
                self.logger.info("Attempting to reconnect and retry query...")
                if self.reconnect():
                    # Retry the query after reconnection
                    try:
                        if processed_params is not None:
                            self.cursor.execute(processed_query, processed_params)
                        else:
                            self.cursor.execute(processed_query)

                        if query.strip().upper().startswith('SELECT'):
                            result = self.cursor.fetchall()
                            self.logger.info(f"SELECT query returned {len(result) if result else 0} rows after reconnection")
                            db_logger.log_query_execution(query, params, success=True)
                            return result
                        else:
                            if not self.in_transaction:
                                self.connection.commit()
                            self.logger.info("Non-SELECT query executed successfully after reconnection")
                            db_logger.log_query_execution(query, params, success=True)
                            return None
                    except Exception as retry_error:
                        error_msg = f"Query failed after reconnection attempt: {str(retry_error)}"
                        self.logger.error(error_msg)
                        db_logger.log_query_execution(query, params, success=False, error_msg=error_msg)
                        raise retry_error
                else:
                    error_msg = "Failed to reconnect to database"
                    self.logger.error(error_msg)
                    db_logger.log_query_execution(query, params, success=False, error_msg=error_msg)
                    raise Exception(error_msg)
            else:
                # For other operational errors, handle normally
                db_logger.log_query_execution(query, params, success=False, error_msg=error_msg)
                # Handle transaction state properly
                if self.in_transaction:
                    # If we're in a transaction and there's an error, we need to rollback the transaction
                    # to prevent the "current transaction is aborted" error
                    try:
                        self.connection.rollback()
                        self.logger.info("Rolled back transaction due to error")
                        self.in_transaction = False  # Reset transaction flag
                    except Exception as rollback_error:
                        self.logger.error(f"Failed to rollback transaction: {rollback_error}")
                else:
                    # Rollback only for non-transaction operations
                    try:
                        self.connection.rollback()
                        self.logger.info("Rolled back transaction due to error")
                    except Exception as rollback_error:
                        self.logger.error(f"Failed to rollback: {rollback_error}")
                raise e
        except psycopg2.Error as e:
            error_msg = f"PostgreSQL error during query execution: {str(e)}"
            self.logger.error(error_msg)
            db_logger.log_query_execution(query, params, success=False, error_msg=error_msg)

            # Handle transaction state properly
            if self.in_transaction:
                # If we're in a transaction and there's an error, we need to rollback the transaction
                # to prevent the "current transaction is aborted" error
                try:
                    self.connection.rollback()
                    self.logger.info("Rolled back transaction due to error")
                    self.in_transaction = False  # Reset transaction flag
                except Exception as rollback_error:
                    self.logger.error(f"Failed to rollback transaction: {rollback_error}")
            else:
                # Rollback only for non-transaction operations
                try:
                    self.connection.rollback()
                    self.logger.info("Rolled back transaction due to error")
                except Exception as rollback_error:
                    self.logger.error(f"Failed to rollback: {rollback_error}")
            raise e
        except Exception as e:
            error_msg = f"Unexpected error during query execution: {str(e)}"
            self.logger.error(error_msg)
            db_logger.log_query_execution(query, params, success=False, error_msg=error_msg)

            # Handle transaction state properly
            if self.in_transaction:
                # If we're in a transaction and there's an error, we need to rollback the transaction
                # to prevent the "current transaction is aborted" error
                try:
                    self.connection.rollback()
                    self.logger.info("Rolled back transaction due to error")
                    self.in_transaction = False  # Reset transaction flag
                except Exception as rollback_error:
                    self.logger.error(f"Failed to rollback transaction: {rollback_error}")
            else:
                # Rollback only for non-transaction operations
                try:
                    self.connection.rollback()
                    self.logger.info("Rolled back transaction due to error")
                except Exception as rollback_error:
                    self.logger.error(f"Failed to rollback: {rollback_error}")
            raise e

    def _is_safe_query(self, query):
        """
        Enhanced check to ensure query doesn't contain dangerous SQL elements.

        Args:
            query (str): SQL query to check

        Returns:
            bool: True if query appears safe, False otherwise
        """
        if not query or not isinstance(query, str):
            return False

        # Normalize the query for checking
        upper_query = query.upper().strip()

        # Check for dangerous patterns anywhere in the query
        dangerous_patterns = [
            'DROP ', 'DROP\t', 'DROP\n', 'TRUNCATE ', 'TRUNCATE\t', 'TRUNCATE\n',
            'DELETE FROM', 'UPDATE ', 'UPDATE\t', 'CREATE ', 'CREATE\t',
            'ALTER ', 'ALTER\t', 'EXECUTE ', 'EXEC ', 'SPOOL ', 'UTL_',
            'DBMS_', 'CTXSYS.', 'ORDSYS.', 'MDSYS.', 'XDB.', 'SYS.',
            'XP_', 'SP_', 'FN_', 'SYS_', 'UNION', 'UNION\t', 'UNION\n',
            'UNION--', 'UNION/*', 'SELECT.*FROM', 'INSERT.*INTO'
        ]

        for pattern in dangerous_patterns:
            if pattern in upper_query:
                return False

        # Additional checks for SQL injection patterns
        # Check for comment indicators that might be used for injection
        if '--' in query or '/*' in query or '*/' in query:
            # But allow them only if they're part of legitimate comments at the end
            parts = query.split('--')
            for part in parts[1:]:  # Skip the first part before --
                if 'DROP' in part.upper() or 'DELETE' in part.upper() or 'UPDATE' in part.upper():
                    return False

        return True

    def get_tables(self):
        """
        Retrieve a list of all table names in the database.

        Returns:
            list: A list of table names in the database
        """
        self.logger.info("Fetching table list from PostgreSQL database")
        try:
            # Check connection before executing query
            if not self.is_connected():
                raise Exception("Database connection is not active")

            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            tables = [table[0] for table in self.cursor.fetchall()]
            self.logger.info(f"Found {len(tables)} tables: {tables}")
            return tables
        except psycopg2.OperationalError as e:
            error_msg = f"PostgreSQL operational error fetching tables: {str(e)}"
            self.logger.error(error_msg)
            # Attempt to reconnect and retry
            if self.reconnect():
                try:
                    self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
                    tables = [table[0] for table in self.cursor.fetchall()]
                    self.logger.info(f"Retried and found {len(tables)} tables: {tables}")
                    return tables
                except Exception as retry_error:
                    self.logger.error(f"Retry failed: {retry_error}")
            return []
        except psycopg2.Error as e:
            error_msg = f"PostgreSQL error fetching tables: {str(e)}"
            self.logger.error(error_msg)
            return []
        except Exception as e:
            error_msg = f"Unexpected error fetching tables: {str(e)}"
            self.logger.error(error_msg)
            return []

    def get_table_info(self, table_name):
        """
        Retrieve detailed information about the columns in a specific table.

        Args:
            table_name (str): Name of the table to get information for

        Returns:
            list: A list of dictionaries containing column information
                  Each dictionary has keys: 'name', 'type', 'not_null', 'default', 'primary_key'

        Raises:
            ValueError: If table_name is invalid
            psycopg2.Error: If a PostgreSQL-specific error occurs
            Exception: If any other error occurs
        """
        if not table_name or not isinstance(table_name, str):
            self.logger.error("Invalid table name provided to get_table_info")
            raise ValueError("Table name must be a non-empty string")

        # Sanitize table name to prevent SQL injection
        if not self._is_safe_identifier(table_name):
            raise ValueError(f"Invalid table name: {table_name}")

        query = """
        SELECT
            c.column_name,
            c.data_type,
            c.is_nullable,
            c.column_default,
            CASE WHEN pk.constraint_type = 'PRIMARY KEY' THEN 1 ELSE 0 END AS is_primary_key
        FROM information_schema.columns c
        LEFT JOIN (
            SELECT kcu.column_name, tc.constraint_type
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY'
        ) pk ON c.column_name = pk.column_name
        WHERE c.table_name = %s
        ORDER BY c.ordinal_position;
        """
        try:
            # Check connection before executing query
            if not self.is_connected():
                raise Exception("Database connection is not active")

            self.cursor.execute(query, (table_name, table_name))
            columns = self.cursor.fetchall()
            result = [{'name': col[0], 'type': col[1], 'not_null': col[2] == 'NO', 'default': col[3], 'primary_key': col[4] == 1} for col in columns]
            self.logger.debug(f"Fetched info for {len(result)} columns in table '{table_name}'")
            return result
        except psycopg2.OperationalError as e:
            error_msg = f"PostgreSQL operational error fetching table info for '{table_name}': {str(e)}"
            self.logger.error(error_msg)
            # Attempt to reconnect and retry
            if self.reconnect():
                try:
                    self.cursor.execute(query, (table_name, table_name))
                    columns = self.cursor.fetchall()
                    result = [{'name': col[0], 'type': col[1], 'not_null': col[2] == 'NO', 'default': col[3], 'primary_key': col[4] == 1} for col in columns]
                    self.logger.debug(f"Retried and fetched info for {len(result)} columns in table '{table_name}'")
                    return result
                except Exception as retry_error:
                    self.logger.error(f"Retry failed: {retry_error}")
                    raise retry_error
            raise e
        except psycopg2.Error as e:
            error_msg = f"PostgreSQL error fetching table info for '{table_name}': {str(e)}"
            self.logger.error(error_msg)
            raise e
        except Exception as e:
            error_msg = f"Unexpected error fetching table info for '{table_name}': {str(e)}"
            self.logger.error(error_msg)
            raise e

    def _is_safe_identifier(self, identifier):
        """
        Check if an identifier (table name, column name, etc.) is safe.

        Args:
            identifier (str): Identifier to check

        Returns:
            bool: True if identifier is safe, False otherwise
        """
        import re
        if not identifier or not isinstance(identifier, str):
            return False

        # PostgreSQL identifier rules: must start with letter or underscore,
        # followed by letters, digits, or underscores, max 63 bytes typically
        # Also check against reserved keywords
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'

        if not re.match(pattern, identifier):
            return False

        # Check against PostgreSQL reserved keywords
        reserved_keywords = {
            'ALL', 'ANALYSE', 'ANALYZE', 'AND', 'ANY', 'ARRAY', 'AS', 'ASC',
            'ASYMMETRIC', 'BOTH', 'CASE', 'CAST', 'CHECK', 'COLLATE', 'COLUMN',
            'CONCURRENTLY', 'CONSTRAINT', 'CREATE', 'CURRENT_CATALOG', 'CURRENT_DATE',
            'CURRENT_ROLE', 'CURRENT_SCHEMA', 'CURRENT_TIME', 'CURRENT_TIMESTAMP',
            'CURRENT_USER', 'DEFAULT', 'DEFERRABLE', 'DESC', 'DISTINCT', 'DO',
            'ELSE', 'END', 'EXCEPT', 'FALSE', 'FETCH', 'FOR', 'FOREIGN', 'FREEZE',
            'FROM', 'FULL', 'GRANT', 'GROUP', 'HAVING', 'ILIKE', 'IN', 'INITIALLY',
            'INNER', 'INTERSECT', 'INTO', 'IS', 'ISNULL', 'JOIN', 'LATERAL', 'LEADING',
            'LEFT', 'LIKE', 'LIMIT', 'LOCALTIME', 'LOCALTIMESTAMP', 'NATURAL', 'NOT',
            'NOTNULL', 'NULL', 'OFFSET', 'ON', 'ONLY', 'OR', 'ORDER', 'OUTER', 'OVERLAPS',
            'PLACING', 'PRIMARY', 'REFERENCES', 'RETURNING', 'RIGHT', 'SELECT', 'SESSION_USER',
            'SIMILAR', 'SOME', 'SYMMETRIC', 'TABLE', 'TABLESAMPLE', 'THEN', 'TO', 'TRAILING',
            'TRUE', 'UNION', 'UNIQUE', 'USER', 'USING', 'VARIADIC', 'VERBOSE', 'WHEN',
            'WHERE', 'WINDOW', 'WITH'
        }

        if identifier.upper() in reserved_keywords:
            return False

        # Limit length to prevent buffer overflow issues
        if len(identifier) > 63:
            return False

        return True

    def table_exists(self, table_name):
        """
        Check if a table exists in the database.

        Args:
            table_name (str): Name of the table to check for existence

        Returns:
            bool: True if the table exists, False otherwise

        Raises:
            ValueError: If table_name is invalid
            psycopg2.Error: If a PostgreSQL-specific error occurs
            Exception: If any other error occurs
        """
        if not table_name or not isinstance(table_name, str):
            self.logger.error("Invalid table name provided to table_exists")
            raise ValueError("Table name must be a non-empty string")

        # Sanitize table name to prevent SQL injection
        if not self._is_safe_identifier(table_name):
            raise ValueError(f"Invalid table name: {table_name}")

        try:
            # Check connection before executing query
            if not self.is_connected():
                raise Exception("Database connection is not active")

            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public' AND tablename = %s;
            """, (table_name,))
            result = cursor.fetchone()
            exists = result is not None
            self.logger.debug(f"Table '{table_name}' exists: {exists}")
            cursor.close()
            return exists
        except psycopg2.OperationalError as e:
            error_msg = f"PostgreSQL operational error checking if table exists '{table_name}': {str(e)}"
            self.logger.error(error_msg)
            # Attempt to reconnect and retry
            if self.reconnect():
                try:
                    cursor = self.connection.cursor()
                    cursor.execute("""
                        SELECT tablename
                        FROM pg_tables
                        WHERE schemaname = 'public' AND tablename = %s;
                    """, (table_name,))
                    result = cursor.fetchone()
                    exists = result is not None
                    self.logger.debug(f"Retried - Table '{table_name}' exists: {exists}")
                    cursor.close()
                    return exists
                except Exception as retry_error:
                    self.logger.error(f"Retry failed: {retry_error}")
                    raise retry_error
            raise e
        except psycopg2.Error as e:
            error_msg = f"PostgreSQL error checking if table exists '{table_name}': {str(e)}"
            self.logger.error(error_msg)
            raise e
        except Exception as e:
            error_msg = f"Unexpected error checking if table exists '{table_name}': {str(e)}"
            self.logger.error(error_msg)
            raise e

    def close(self):
        """
        Close the database connection.
        """
        try:
            if self.connection:
                # Check if connection is still active before closing
                if self.is_connected():
                    self.connection.close()
                    self.logger.info("Database connection closed successfully")
                else:
                    self.logger.info("Database connection was already closed")
        except Exception as e:
            self.logger.error(f"Error closing database connection: {str(e)}")
            # Attempt to force close if normal close failed
            try:
                if self.connection:
                    self.connection.rollback()  # Rollback any pending transactions
                    self.connection.close()
            except:
                pass  # Ignore errors during forced close

    def begin_transaction(self):
        """
        Start a new database transaction.

        Returns:
            bool: True if transaction started successfully, False otherwise
        """
        if self.in_transaction:
            self.logger.warning("Already in a transaction. Nested transactions not supported in this implementation.")
            return False
        try:
            self.cursor.execute("BEGIN")
            self.in_transaction = True
            self.logger.info("Transaction started successfully")
            return True
        except psycopg2.Error as e:
            error_msg = f"PostgreSQL error beginning transaction: {str(e)}"
            self.logger.error(error_msg)
            return False
        except Exception as e:
            error_msg = f"Unexpected error beginning transaction: {str(e)}"
            self.logger.error(error_msg)
            return False

    def commit_transaction(self):
        """
        Commit the current database transaction.

        Returns:
            bool: True if transaction committed successfully, False otherwise
        """
        if not self.in_transaction:
            self.logger.warning("No active transaction to commit.")
            return False
        try:
            self.connection.commit()
            self.in_transaction = False
            self.logger.info("Transaction committed successfully")
            return True
        except psycopg2.Error as e:
            error_msg = f"PostgreSQL error committing transaction: {str(e)}"
            self.logger.error(error_msg)
            return False
        except Exception as e:
            error_msg = f"Unexpected error committing transaction: {str(e)}"
            self.logger.error(error_msg)
            return False

    def rollback_transaction(self):
        """
        Rollback the current database transaction.

        Returns:
            bool: True if transaction rolled back successfully, False otherwise
        """
        if not self.in_transaction:
            self.logger.warning("No active transaction to rollback.")
            return False
        try:
            self.connection.rollback()
            self.in_transaction = False
            self.logger.info("Transaction rolled back successfully")
            return True
        except psycopg2.Error as e:
            error_msg = f"PostgreSQL error rolling back transaction: {str(e)}"
            self.logger.error(error_msg)
            return False
        except Exception as e:
            error_msg = f"Unexpected error rolling back transaction: {str(e)}"
            self.logger.error(error_msg)
            return False

    def execute_transaction(self, queries_list):
        """
        Execute a list of queries as a single database transaction.

        Args:
            queries_list (list): A list of queries to execute as a transaction.
                               Each item can be a string (query) or a tuple (query, params)

        Returns:
            list: Results from each query in the transaction

        Raises:
            ValueError: If queries_list is not a list or is empty
            Exception: If the transaction fails and is rolled back
        """
        if not isinstance(queries_list, list):
            error_msg = "Error: Queries must be provided as a list."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        if not queries_list:
            error_msg = "Error: Queries list cannot be empty."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # Check if already in a transaction to prevent nested transactions
        if self.in_transaction:
            error_msg = "Error: Already in a transaction. Cannot start a new transaction."
            self.logger.error(error_msg)
            raise Exception(error_msg)

        try:
            self.logger.info(f"Starting transaction with {len(queries_list)} queries")

            # Begin the transaction
            if not self.begin_transaction():
                raise Exception("Failed to begin transaction")

            results = []
            for i, query_info in enumerate(queries_list):
                if isinstance(query_info, str):
                    query = query_info
                    params = None
                elif isinstance(query_info, tuple) and len(query_info) >= 1:
                    query = query_info[0]
                    params = query_info[1] if len(query_info) > 1 else None
                else:
                    error_msg = f"Each query at index {i} should be a string or a tuple of (query, params)"
                    self.logger.error(error_msg)
                    # Rollback the transaction before raising the error
                    self.rollback_transaction()
                    raise ValueError(error_msg)

                try:
                    result = self.execute_query(query, params)
                    results.append(result)
                except Exception as query_error:
                    # If any query fails, rollback the entire transaction
                    self.logger.error(f"Query at index {i} failed: {str(query_error)}")
                    self.rollback_transaction()
                    raise query_error

            success = self.commit_transaction()
            if success:
                self.logger.info(f"Transaction completed successfully with {len(results)} operations")
                return results
            else:
                raise Exception("Failed to commit transaction")
        except Exception as e:
            # Ensure transaction is rolled back in case of any error
            if self.in_transaction:
                try:
                    self.rollback_transaction()
                except Exception as rollback_error:
                    self.logger.error(f"Error during rollback: {rollback_error}")
            error_msg = f"Transaction failed and was rolled back: {str(e)}"
            self.logger.error(error_msg)
            raise e


    def execute_prepared_query(self, query, params=None):
        """
        Execute a prepared statement query for better performance and security.

        Args:
            query (str): The SQL query to execute
            params (tuple or list, optional): Parameters to bind to the query

        Returns:
            list or None: Query results for SELECT queries, None for others

        Raises:
            ValueError: If query is invalid
            psycopg2.Error: If a PostgreSQL-specific error occurs
            Exception: If any other error occurs
        """
        try:
            self.logger.debug(f"Executing prepared query: {query[:100]}...")  # First 100 characters of the query

            # Validate inputs
            if not query or not isinstance(query, str):
                raise ValueError("Query must be a non-empty string")

            # Execute the query with parameters
            if params is not None:
                self.logger.debug(f"With parameters: {[str(p)[:50] + '...' if len(str(p)) > 50 else str(p) for p in params]}")
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                result = self.cursor.fetchall()
                self.logger.info(f"SELECT query returned {len(result) if result else 0} rows")
                db_logger.log_query_execution(query, params, success=True)
                return result
            else:
                # Only commit if not in an active transaction
                if not self.in_transaction:
                    self.connection.commit()
                self.logger.info("Non-SELECT query executed successfully")
                db_logger.log_query_execution(query, params, success=True)
                return None
        except psycopg2.Error as e:
            error_msg = f"PostgreSQL error during prepared query execution: {str(e)}"
            self.logger.error(error_msg)
            db_logger.log_query_execution(query, params, success=False, error_msg=error_msg)

            # Handle transaction state properly
            if self.in_transaction:
                pass  # Let calling code handle transaction
            else:
                # Rollback only for non-transaction operations
                try:
                    self.connection.rollback()
                    self.logger.info("Rolled back transaction due to error")
                except Exception as rollback_error:
                    self.logger.error(f"Failed to rollback: {rollback_error}")
            raise e
        except Exception as e:
            error_msg = f"Unexpected error during prepared query execution: {str(e)}"
            self.logger.error(error_msg)
            db_logger.log_query_execution(query, params, success=False, error_msg=error_msg)

            # Handle transaction state properly
            if self.in_transaction:
                pass  # Let calling code handle transaction
            else:
                # Rollback only for non-transaction operations
                try:
                    self.connection.rollback()
                    self.logger.info("Rolled back transaction due to error")
                except Exception as rollback_error:
                    self.logger.error(f"Failed to rollback: {rollback_error}")
            raise e


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data if data else []
        self._headers = [] if not data else [str(i) for i in range(len(data[0]))] if data else []

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers) if self._headers else (len(self._data[0]) if self._data else 0)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._headers[section] if section < len(self._headers) else str(section)
        return super().headerData(section, orientation, role)