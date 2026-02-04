import logging
import os
from datetime import datetime


class DatabaseLogger:
    """Handles logging for database connection and operations"""
    
    def __init__(self):
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with file and console handlers"""
        logger = logging.getLogger('DatabaseManager')
        logger.setLevel(logging.DEBUG)
        
        # Avoid adding handlers multiple times
        if logger.handlers:
            return logger
        
        # Ensure logs directory exists
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # File handler
        log_file = os.path.join(log_dir, f"db_connections_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_connection_attempt(self, db_type, connection_params, success, error_msg=None):
        """Log database connection attempts"""
        if success:
            self.logger.info(f"Successfully connected to {db_type} database")
            self.logger.debug(f"Connection parameters: {self._sanitize_params(connection_params)}")
        else:
            self.logger.error(f"Failed to connect to {db_type} database: {error_msg}")
            self.logger.debug(f"Failed connection parameters: {self._sanitize_params(connection_params)}")
    
    def log_query_execution(self, query, params=None, success=True, error_msg=None, row_count=None):
        """Log query execution"""
        if success:
            if row_count is not None:
                self.logger.debug(f"Query executed successfully: {query[:100]}..., Rows affected: {row_count}")  # First 100 chars
            else:
                self.logger.debug(f"Query executed successfully: {query[:100]}...")  # First 100 chars
        else:
            self.logger.error(f"Query execution failed: {query[:100]}..., Error: {error_msg}")
    
    def _sanitize_params(self, params):
        """Sanitize connection parameters to hide sensitive information"""
        if not isinstance(params, dict):
            return params
            
        sanitized = params.copy()
        if 'password' in sanitized:
            sanitized['password'] = '[HIDDEN]'
        return sanitized


# Global logger instance
db_logger = DatabaseLogger()