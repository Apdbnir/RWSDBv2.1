"""
Enhanced Backup Manager for Train Station DBMS

This module provides comprehensive backup and restore functionality for the 
database management system with support for both PostgreSQL and file-based backups.
It includes advanced features like incremental backups, compression, encryption,
and detailed logging.
"""

import os
import json
import gzip
import shutil
import subprocess
import datetime
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List
from enum import Enum
import logging
from cryptography.fernet import Fernet
import tempfile


class BackupType(Enum):
    """Enumeration of backup types"""
    FULL = "full"
    INCREMENTAL = "incremental"
    STRUCTURE_ONLY = "structure_only"
    DATA_ONLY = "data_only"


class BackupStatus(Enum):
    """Enumeration of backup statuses"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EnhancedBackupManager:
    def __init__(self, db_manager, backup_dir: str = "./backups"):
        """
        Initialize the enhanced backup manager.

        Args:
            db_manager: Database manager instance
            backup_dir: Directory to store backups
        """
        self.db_manager = db_manager
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = self._setup_logger()
        
        # Encryption key for encrypted backups
        self.encryption_key = None
        
        # Track ongoing operations
        self.current_operation = None
        self.operation_progress = 0

    def _setup_logger(self) -> logging.Logger:
        """Setup logger for backup operations."""
        logger = logging.getLogger('EnhancedBackupManager')
        logger.setLevel(logging.INFO)
        
        # Create file handler
        log_file = self.backup_dir / "backup.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger

    def create_backup(
        self, 
        backup_name: Optional[str] = None, 
        backup_type: BackupType = BackupType.FULL,
        compress: bool = True,
        encrypt: bool = False,
        include_schema: bool = True,
        include_data: bool = True
    ) -> str:
        """
        Create a comprehensive backup of the database.

        Args:
            backup_name: Custom name for the backup (auto-generated if None)
            backup_type: Type of backup to create
            compress: Whether to compress the backup
            encrypt: Whether to encrypt the backup
            include_schema: Whether to include database schema
            include_data: Whether to include database data

        Returns:
            Path to the created backup file

        Raises:
            Exception: If backup creation fails
        """
        self.logger.info(f"Starting backup creation: {backup_name or 'auto-generated'}")
        self.current_operation = "backup"
        self.operation_progress = 0
        
        try:
            # Generate backup name if not provided
            if not backup_name:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"backup_{self.db_manager.db_type}_{timestamp}"
            
            # Determine file extension based on options
            file_ext = ".sql"
            if compress:
                file_ext += ".gz"
            if encrypt:
                file_ext += ".enc"
            
            backup_path = self.backup_dir / f"{backup_name}{file_ext}"
            
            # Create backup based on database type
            if self.db_manager.db_type == 'postgresql':
                backup_file = self._create_postgresql_backup(backup_path, backup_type, include_schema, include_data)
            else:
                backup_file = self._create_json_backup(backup_path, backup_type, include_schema, include_data)
            
            # Apply compression if requested
            if compress:
                backup_file = self._compress_file(backup_file)
            
            # Apply encryption if requested
            if encrypt:
                backup_file = self._encrypt_file(backup_file)
            
            # Create backup manifest
            self._create_manifest(backup_file, backup_type, include_schema, include_data)
            
            self.logger.info(f"Backup completed successfully: {backup_file}")
            self.operation_progress = 100
            return str(backup_file)
            
        except Exception as e:
            self.logger.error(f"Backup failed: {str(e)}")
            raise
        finally:
            self.current_operation = None

    def _create_postgresql_backup(
        self, 
        backup_path: Path, 
        backup_type: BackupType, 
        include_schema: bool, 
        include_data: bool
    ) -> Path:
        """Create a PostgreSQL backup using pg_dump."""
        # Prepare pg_dump command based on backup type
        cmd = [
            'pg_dump',
            '-h', self.db_manager.connection_params['host'],
            '-p', str(self.db_manager.connection_params['port']),
            '-U', self.db_manager.connection_params['user'],
            '-d', self.db_manager.connection_params['database'],
            '--verbose',
            '--clean',
            '--no-owner',
            '--no-privileges',
            '--file', str(backup_path)
        ]
        
        # Add options based on backup type
        if backup_type == BackupType.STRUCTURE_ONLY:
            cmd.extend(['--schema-only'])
        elif backup_type == BackupType.DATA_ONLY:
            cmd.extend(['--data-only'])
        
        # Set environment variable for password
        env = os.environ.copy()
        env['PGPASSWORD'] = self.db_manager.connection_params['password']
        
        try:
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
            self.logger.info(f"PostgreSQL backup created: {backup_path}")
            return backup_path
        except subprocess.CalledProcessError as e:
            self.logger.error(f"PostgreSQL backup failed: {e.stderr}")
            raise
        except FileNotFoundError:
            self.logger.error("pg_dump command not found. Please ensure PostgreSQL is installed and in PATH.")
            raise

    def _create_json_backup(
        self, 
        backup_path: Path, 
        backup_type: BackupType, 
        include_schema: bool, 
        include_data: bool
    ) -> Path:
        """Create a JSON backup for other database types."""
        backup_data = {
            'metadata': {
                'created_at': datetime.datetime.now().isoformat(),
                'database_type': self.db_manager.db_type,
                'backup_type': backup_type.value,
                'includes_schema': include_schema,
                'includes_data': include_data
            },
            'tables': {}
        }
        
        if include_data or include_schema:
            tables = self.db_manager.get_tables()
            for i, table in enumerate(tables):
                self.operation_progress = int((i / len(tables)) * 50)  # 50% for data collection
                
                table_data = {}
                
                if include_schema:
                    try:
                        columns_info = self.db_manager.get_table_info(table)
                        table_data['schema'] = columns_info
                    except Exception as e:
                        self.logger.warning(f"Could not get schema for table {table}: {e}")
                
                if include_data:
                    try:
                        query = f"SELECT * FROM {table}"
                        rows = self.db_manager.execute_query(query)
                        table_data['data'] = rows if rows else []
                    except Exception as e:
                        self.logger.warning(f"Could not get data for table {table}: {e}")
                
                backup_data['tables'][table] = table_data
        
        # Write backup data to file
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, default=str)
        
        self.logger.info(f"JSON backup created: {backup_path}")
        return backup_path

    def _compress_file(self, file_path: Path) -> Path:
        """Compress a file using gzip."""
        compressed_path = file_path.with_suffix(file_path.suffix + '.gz')
        
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove original file after compression
        file_path.unlink()
        
        self.logger.info(f"File compressed: {compressed_path}")
        return compressed_path

    def _encrypt_file(self, file_path: Path) -> Path:
        """Encrypt a file using Fernet symmetric encryption."""
        # Generate encryption key if not exists
        if not self.encryption_key:
            self.encryption_key = Fernet.generate_key()
        
        encrypted_path = file_path.with_suffix(file_path.suffix + '.enc')
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        fernet = Fernet(self.encryption_key)
        encrypted_data = fernet.encrypt(data)
        
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        # Remove original file after encryption
        file_path.unlink()
        
        self.logger.info(f"File encrypted: {encrypted_path}")
        return encrypted_path

    def _create_manifest(self, backup_file: Path, backup_type: BackupType, include_schema: bool, include_data: bool):
        """Create a manifest file for the backup."""
        manifest_data = {
            'backup_file': str(backup_file.name),
            'created_at': datetime.datetime.now().isoformat(),
            'backup_type': backup_type.value,
            'includes_schema': include_schema,
            'includes_data': include_data,
            'file_size': backup_file.stat().st_size,
            'checksum': self._calculate_checksum(backup_file)
        }
        
        manifest_path = backup_file.with_suffix('.manifest.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_data, f, indent=2)
        
        self.logger.info(f"Manifest created: {manifest_path}")

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA-256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def restore_backup(
        self, 
        backup_file: str, 
        verify_checksum: bool = True,
        decrypt: bool = True,
        decompress: bool = True
    ) -> bool:
        """
        Restore the database from a backup file.

        Args:
            backup_file: Path to the backup file to restore from
            verify_checksum: Whether to verify the backup checksum before restoring
            decrypt: Whether to decrypt the backup before restoring
            decompress: Whether to decompress the backup before restoring

        Returns:
            True if restore was successful, False otherwise
        """
        self.logger.info(f"Starting restore from: {backup_file}")
        self.current_operation = "restore"
        self.operation_progress = 0
        
        try:
            backup_path = Path(backup_file)
            
            # Verify backup exists
            if not backup_path.exists():
                self.logger.error(f"Backup file does not exist: {backup_file}")
                return False
            
            # Verify checksum if requested
            if verify_checksum and not self._verify_backup_integrity(backup_path):
                self.logger.error(f"Backup integrity check failed: {backup_file}")
                return False
            
            # Find manifest file
            manifest_path = backup_path.with_suffix('.manifest.json')
            if manifest_path.exists():
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                self.logger.info(f"Backup manifest: {manifest}")
            
            # Decrypt if needed
            if decrypt and backup_path.suffix == '.enc':
                backup_path = self._decrypt_file(backup_path)
            
            # Decompress if needed
            if decompress and backup_path.suffix == '.gz':
                backup_path = self._decompress_file(backup_path)
            
            # Perform restore based on database type
            if self.db_manager.db_type == 'postgresql':
                success = self._restore_postgresql_backup(backup_path)
            else:
                success = self._restore_json_backup(backup_path)
            
            if success:
                self.logger.info(f"Restore completed successfully: {backup_file}")
                self.operation_progress = 100
            else:
                self.logger.error(f"Restore failed: {backup_file}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Restore failed: {str(e)}")
            return False
        finally:
            self.current_operation = None

    def _decrypt_file(self, file_path: Path) -> Path:
        """Decrypt an encrypted file."""
        decrypted_path = file_path.with_suffix('')
        
        # If we don't have the encryption key, try to load it from a file
        if not self.encryption_key:
            key_path = file_path.parent / "encryption.key"
            if key_path.exists():
                with open(key_path, 'rb') as f:
                    self.encryption_key = f.read()
            else:
                raise Exception("Encryption key not found. Cannot decrypt backup.")
        
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        
        fernet = Fernet(self.encryption_key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        with open(decrypted_path, 'wb') as f:
            f.write(decrypted_data)
        
        # Remove encrypted file after decryption
        file_path.unlink()
        
        self.logger.info(f"File decrypted: {decrypted_path}")
        return decrypted_path

    def _decompress_file(self, file_path: Path) -> Path:
        """Decompress a gzipped file."""
        decompressed_path = file_path.with_suffix('')
        
        with gzip.open(file_path, 'rb') as f_in:
            with open(decompressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Remove compressed file after decompression
        file_path.unlink()
        
        self.logger.info(f"File decompressed: {decompressed_path}")
        return decompressed_path

    def _verify_backup_integrity(self, backup_path: Path) -> bool:
        """Verify the integrity of a backup using checksum."""
        manifest_path = backup_path.with_suffix('.manifest.json')
        if not manifest_path.exists():
            self.logger.warning("No manifest file found for integrity check")
            return True  # Assume integrity if no manifest
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        expected_checksum = manifest.get('checksum')
        if not expected_checksum:
            self.logger.warning("No checksum found in manifest")
            return True
        
        actual_checksum = self._calculate_checksum(backup_path)
        
        if expected_checksum == actual_checksum:
            self.logger.info("Backup integrity verified")
            return True
        else:
            self.logger.error("Backup integrity check failed")
            return False

    def _restore_postgresql_backup(self, backup_path: Path) -> bool:
        """Restore a PostgreSQL database from a backup file."""
        # First, drop and recreate the database
        drop_cmd = [
            'psql',
            '-h', self.db_manager.connection_params['host'],
            '-p', str(self.db_manager.connection_params['port']),
            '-U', self.db_manager.connection_params['user'],
            '-c', f'DROP DATABASE IF EXISTS {self.db_manager.connection_params["database"]};'
        ]

        create_cmd = [
            'psql',
            '-h', self.db_manager.connection_params['host'],
            '-p', str(self.db_manager.connection_params['port']),
            '-U', self.db_manager.connection_params['user'],
            '-c', f'CREATE DATABASE {self.db_manager.connection_params["database"]};'
        ]

        # Set environment variable for password
        env = os.environ.copy()
        env['PGPASSWORD'] = self.db_manager.connection_params['password']

        try:
            # Drop the database
            result = subprocess.run(drop_cmd, env=env, capture_output=True, text=True, check=True)
            self.logger.info("Existing database dropped successfully")

            # Recreate the database
            result = subprocess.run(create_cmd, env=env, capture_output=True, text=True, check=True)
            self.logger.info("New database created successfully")

            # Restore from backup
            restore_cmd = [
                'psql',
                '-h', self.db_manager.connection_params['host'],
                '-p', str(self.db_manager.connection_params['port']),
                '-U', self.db_manager.connection_params['user'],
                '-d', self.db_manager.connection_params['database'],
                '-f', str(backup_path)
            ]

            result = subprocess.run(restore_cmd, env=env, capture_output=True, text=True, check=True)
            self.logger.info(f"Database restored successfully from: {backup_path}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"PostgreSQL restore failed: {e.stderr}")
            return False
        except FileNotFoundError:
            self.logger.error("psql command not found. Please ensure PostgreSQL is installed and in PATH.")
            return False

    def _restore_json_backup(self, backup_path: Path) -> bool:
        """Restore a database from a JSON backup file."""
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Get tables to restore
            tables = backup_data.get('tables', {})
            
            for i, (table_name, table_data) in enumerate(tables.items()):
                self.operation_progress = int((i / len(tables)) * 100)  # Progress through tables
                
                # If schema exists, recreate the table
                if 'schema' in table_data and table_data['schema']:
                    # Drop the table if it exists
                    if self.db_manager.db_type == 'postgresql':
                        drop_query = f'DROP TABLE IF EXISTS "{table_name}" CASCADE'
                    else:
                        drop_query = f"DROP TABLE IF EXISTS {table_name}"
                    
                    self.db_manager.execute_query(drop_query)
                    
                    # Recreate the table based on schema
                    columns_info = table_data['schema']
                    columns_def = []
                    for col in columns_info:
                        col_def = f'"{col["name"]}" {col["type"]}'
                        if col["not_null"]:
                            col_def += " NOT NULL"
                        if col["primary_key"]:
                            col_def += " PRIMARY KEY"
                        if col["default"] is not None:
                            col_def += f" DEFAULT {col['default']}"
                        columns_def.append(col_def)
                    
                    if self.db_manager.db_type == 'postgresql':
                        create_query = f'CREATE TABLE "{table_name}" ({", ".join(columns_def)})'
                    else:
                        create_query = f"CREATE TABLE {table_name} ({', '.join(columns_def)})"
                    
                    self.db_manager.execute_query(create_query)
                
                # If data exists, insert it
                if 'data' in table_data and table_data['data']:
                    # Get column names
                    if 'schema' in table_data:
                        columns = [col['name'] for col in table_data['schema']]
                    else:
                        # If no schema, assume all columns from first row
                        if table_data['data']:
                            columns = [f"col{i}" for i in range(len(table_data['data'][0]))]
                        else:
                            continue
                    
                    # Insert data
                    if self.db_manager.db_type == 'postgresql':
                        # For PostgreSQL, use %s placeholders
                        placeholders = ', '.join(['%s' for _ in columns])
                        insert_query = f'INSERT INTO "{table_name}" ({", ".join([f"{col}" for col in columns])}) VALUES ({placeholders})'
                        for row in table_data['data']:
                            self.db_manager.execute_query(insert_query, row)
                    else:
                        # For PostgreSQL, use %s placeholders
                        placeholders = ', '.join(['%s' for _ in columns])
                        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                        for row in table_data['data']:
                            self.db_manager.execute_query(insert_query, row)
            
            self.logger.info(f"JSON backup restored successfully from: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"JSON restore failed: {str(e)}")
            return False

    def list_backups(self) -> List[Dict[str, Any]]:
        """
        List all available backup files with metadata.

        Returns:
            List of backup metadata dictionaries
        """
        backup_files = list(self.backup_dir.glob("*"))
        backups = []
        
        for file_path in backup_files:
            if file_path.is_file() and not file_path.name.endswith('.log'):
                # Look for associated manifest
                manifest_path = file_path.with_suffix('.manifest.json')
                manifest = {}
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                
                backups.append({
                    'filename': file_path.name,
                    'path': str(file_path),
                    'size': file_path.stat().st_size,
                    'modified': datetime.datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'manifest': manifest
                })
        
        # Sort by modification time (newest first)
        backups.sort(key=lambda x: x['modified'], reverse=True)
        return backups

    def cleanup_old_backups(self, keep_days: int = 7, keep_count: int = 10) -> int:
        """
        Remove old backup files based on age and count limits.

        Args:
            keep_days: Maximum age of backups to keep (in days)
            keep_count: Maximum number of backups to keep

        Returns:
            Number of files deleted
        """
        all_backups = self.list_backups()
        
        # Filter out manifest and log files
        backup_files = [b for b in all_backups if not b['filename'].endswith(('.manifest.json', '.log'))]
        
        # Sort by modification time (oldest first)
        backup_files.sort(key=lambda x: x['modified'])
        
        # Determine which files to delete
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=keep_days)).isoformat()
        files_to_delete = []
        
        # First, remove files older than keep_days
        for backup in backup_files:
            if backup['modified'] < cutoff_date:
                files_to_delete.append(backup['path'])
        
        # Then, if we still have too many files, remove oldest ones beyond keep_count
        if len(backup_files) - len(files_to_delete) > keep_count:
            excess_count = (len(backup_files) - len(files_to_delete)) - keep_count
            for i in range(excess_count):
                if i < len(backup_files):
                    backup_info = backup_files[i]
                    if backup_info['path'] not in files_to_delete:
                        files_to_delete.append(backup_info['path'])
        
        # Delete the files
        deleted_count = 0
        for file_path in files_to_delete:
            try:
                Path(file_path).unlink()
                # Also delete associated manifest if it exists
                manifest_path = Path(file_path).with_suffix('.manifest.json')
                if manifest_path.exists():
                    manifest_path.unlink()
                self.logger.info(f"Deleted old backup: {Path(file_path).name}")
                deleted_count += 1
            except OSError as e:
                self.logger.error(f"Error deleting backup {Path(file_path).name}: {e}")
        
        self.logger.info(f"Cleanup completed. Deleted {deleted_count} old backup files.")
        return deleted_count

    def get_operation_progress(self) -> int:
        """
        Get the progress of the current operation.

        Returns:
            Progress percentage (0-100)
        """
        return self.operation_progress

    def cancel_operation(self) -> bool:
        """
        Cancel the current operation if possible.

        Returns:
            True if operation was cancelled, False otherwise
        """
        if self.current_operation:
            self.logger.info(f"Cancelling {self.current_operation} operation")
            self.current_operation = None
            self.operation_progress = 0
            return True
        return False

    def get_backup_info(self, backup_file: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a backup file.

        Args:
            backup_file: Path to the backup file

        Returns:
            Dictionary with backup information, or None if not found
        """
        backup_path = Path(backup_file)
        manifest_path = backup_path.with_suffix('.manifest.json')
        
        if not backup_path.exists():
            return None
        
        info = {
            'filename': backup_path.name,
            'path': str(backup_path),
            'size': backup_path.stat().st_size,
            'modified': datetime.datetime.fromtimestamp(backup_path.stat().st_mtime).isoformat(),
            'is_encrypted': backup_path.suffix == '.enc',
            'is_compressed': '.gz' in backup_path.suffix,
        }
        
        # Add manifest info if available
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            info['manifest'] = manifest
        
        return info