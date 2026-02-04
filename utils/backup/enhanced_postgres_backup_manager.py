"""
Enhanced PostgreSQL Backup Manager for Train Station DBMS
Provides robust backup and restore functionality for PostgreSQL database with improved error handling
"""

import os
import subprocess
import datetime
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from enum import Enum


class BackupStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"


class BackupInfo:
    """Class to store backup metadata"""
    def __init__(self, filename: str, size: int, timestamp: datetime.datetime, 
                 status: BackupStatus, description: str = ""):
        self.filename = filename
        self.size = size
        self.timestamp = timestamp
        self.status = status
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            'filename': self.filename,
            'size': self.size,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status.value,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            filename=data['filename'],
            size=data['size'],
            timestamp=datetime.datetime.fromisoformat(data['timestamp']),
            status=BackupStatus(data['status']),
            description=data.get('description', '')
        )


class EnhancedPostgreSQLBackupManager:
    def __init__(self, db_config: Dict[str, Any], backup_dir: str = './backups/postgres'):
        """
        Initialize the enhanced PostgreSQL backup manager

        Args:
            db_config: Dictionary containing database configuration
                      Expected keys: host, port, database, user, password
            backup_dir: Directory to store backup files
        """
        self.db_config = db_config
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.backup_log_file = self.backup_dir / 'backup_log.json'
        
        # Load existing backup log
        self.backup_log = self._load_backup_log()

    def _load_backup_log(self) -> Dict[str, Any]:
        """Load backup log from file"""
        if self.backup_log_file.exists():
            try:
                with open(self.backup_log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.logger.warning(f"Could not load backup log: {e}")
                return {'backups': [], 'settings': {}}
        return {'backups': [], 'settings': {}}

    def _save_backup_log(self):
        """Save backup log to file"""
        try:
            with open(self.backup_log_file, 'w', encoding='utf-8') as f:
                json.dump(self.backup_log, f, ensure_ascii=False, indent=2)
        except IOError as e:
            self.logger.error(f"Could not save backup log: {e}")

    def _record_backup(self, backup_info: BackupInfo):
        """Record backup information in the log"""
        backup_entry = backup_info.to_dict()
        self.backup_log['backups'].append(backup_entry)
        self._save_backup_log()

    def create_backup(self, backup_name: Optional[str] = None, 
                     include_data: bool = True, 
                     include_schema: bool = True,
                     compress: bool = True,
                     description: str = "") -> str:
        """
        Create a backup of the PostgreSQL database with enhanced options

        Args:
            backup_name: Optional custom name for the backup
            include_data: Whether to include table data in backup
            include_schema: Whether to include schema definitions
            compress: Whether to compress the backup
            description: Description for the backup

        Returns:
            Path to the created backup file
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if backup_name:
            filename = f"{backup_name}_{timestamp}.sql"
        else:
            filename = f"{self.db_config['database']}_backup_{timestamp}.sql"

        backup_path = self.backup_dir / filename

        # Prepare pg_dump command with enhanced options
        cmd = [
            'pg_dump',
            '-h', self.db_config['host'],
            '-p', str(self.db_config['port']),
            '-U', self.db_config['user'],
            '-d', self.db_config['database'],
            '--verbose',
            '--clean',
            '--no-owner',
            '--no-privileges'
        ]

        # Add options based on parameters
        if not include_data:
            cmd.extend(['--schema-only'])
        if compress:
            cmd.extend(['--compress', '6'])  # Compression level 6 (default is 6)

        cmd.extend(['--file', str(backup_path)])

        # Set environment variable for password
        env = os.environ.copy()
        env['PGPASSWORD'] = self.db_config['password']

        # Record backup start
        backup_info = BackupInfo(
            filename=str(backup_path),
            size=0,
            timestamp=datetime.datetime.now(),
            status=BackupStatus.IN_PROGRESS,
            description=description
        )
        self._record_backup(backup_info)

        try:
            self.logger.info(f"Starting backup: {backup_path}")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
            
            # Update backup info after successful completion
            backup_info.size = backup_path.stat().st_size
            backup_info.status = BackupStatus.SUCCESS
            
            # Update the log entry
            for entry in reversed(self.backup_log['backups']):  # Find the most recent entry
                if entry['filename'] == str(backup_path) and entry['status'] == BackupStatus.IN_PROGRESS.value:
                    entry.update(backup_info.to_dict())
                    break
            
            self._save_backup_log()
            
            self.logger.info(f"Backup created successfully: {backup_path}")
            self.logger.info(f"Backup size: {backup_info.size} bytes")
            return str(backup_path)
        except subprocess.CalledProcessError as e:
            # Update status to failed
            backup_info.status = BackupStatus.FAILED
            for entry in reversed(self.backup_log['backups']):
                if entry['filename'] == str(backup_path) and entry['status'] == BackupStatus.IN_PROGRESS.value:
                    entry.update(backup_info.to_dict())
                    break
            self._save_backup_log()
            
            error_msg = f"Backup failed: {e.stderr if e.stderr else str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        except FileNotFoundError:
            error_msg = "Error: pg_dump command not found. Please ensure PostgreSQL is installed and in PATH."
            self.logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            # Update status to failed
            backup_info.status = BackupStatus.FAILED
            for entry in reversed(self.backup_log['backups']):
                if entry['filename'] == str(backup_path) and entry['status'] == BackupStatus.IN_PROGRESS.value:
                    entry.update(backup_info.to_dict())
                    break
            self._save_backup_log()
            
            error_msg = f"Unexpected error during backup: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def restore_backup(self, backup_file: str, 
                      verify_checksum: bool = True,
                      dry_run: bool = False) -> bool:
        """
        Restore the PostgreSQL database from a backup file with verification

        Args:
            backup_file: Path to the backup file to restore from
            verify_checksum: Whether to verify the backup file integrity
            dry_run: Whether to perform a dry run without actually restoring

        Returns:
            True if restore was successful, False otherwise
        """
        backup_path = Path(backup_file)
        if not backup_path.exists():
            error_msg = f"Error: Backup file does not exist: {backup_file}"
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        # Verify backup file integrity if requested
        if verify_checksum:
            if not self._verify_backup_integrity(backup_path):
                error_msg = f"Backup file integrity check failed: {backup_file}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

        # If dry run, just return True without performing actual restore
        if dry_run:
            self.logger.info(f"Dry run: Would restore from {backup_file}")
            return True

        # Set environment variable for password
        env = os.environ.copy()
        env['PGPASSWORD'] = self.db_config['password']

        try:
            self.logger.info(f"Starting restore from: {backup_file}")

            # First, drop and recreate the database
            drop_cmd = [
                'psql',
                '-h', self.db_config['host'],
                '-p', str(self.db_config['port']),
                '-U', self.db_config['user'],
                '-c', f'DROP DATABASE IF EXISTS {self.db_config["database"]};'
            ]

            create_cmd = [
                'psql',
                '-h', self.db_config['host'],
                '-p', str(self.db_config['port']),
                '-U', self.db_config['user'],
                '-c', f'CREATE DATABASE {self.db_config["database"]};'
            ]

            # Drop the database
            result = subprocess.run(drop_cmd, env=env, capture_output=True, text=True, check=True)
            self.logger.info("Existing database dropped successfully")

            # Recreate the database
            result = subprocess.run(create_cmd, env=env, capture_output=True, text=True, check=True)
            self.logger.info("New database created successfully")

            # Restore from backup
            restore_cmd = [
                'psql',
                '-h', self.db_config['host'],
                '-p', str(self.db_config['port']),
                '-U', self.db_config['user'],
                '-d', self.db_config['database'],
                '-v', 'ON_ERROR_STOP=1',  # Stop on error
                '-f', str(backup_path)
            ]

            result = subprocess.run(restore_cmd, env=env, capture_output=True, text=True, check=True)
            self.logger.info(f"Database restored successfully from: {backup_file}")
            return True
        except subprocess.CalledProcessError as e:
            error_msg = f"Restore failed: {e.stderr if e.stderr else str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        except FileNotFoundError:
            error_msg = "Error: psql command not found. Please ensure PostgreSQL is installed and in PATH."
            self.logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error during restore: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def _verify_backup_integrity(self, backup_path: Path) -> bool:
        """
        Verify the integrity of a backup file by checking if it contains valid SQL

        Args:
            backup_path: Path to the backup file to verify

        Returns:
            True if the backup appears to be valid, False otherwise
        """
        try:
            # Check if file is not empty
            if backup_path.stat().st_size == 0:
                self.logger.warning(f"Backup file is empty: {backup_path}")
                return False

            # Check if file starts with typical pg_dump header
            with open(backup_path, 'r', encoding='utf-8', errors='ignore') as f:
                header = f.read(1000)  # Read first 1000 characters

            # Look for typical pg_dump markers
            if 'PostgreSQL database dump' not in header and 'pg_dump' not in header:
                self.logger.warning(f"Backup file doesn't appear to be a valid pg_dump: {backup_path}")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Error verifying backup integrity: {e}")
            return False

    def list_backups(self, include_failed: bool = False) -> List[Dict[str, Any]]:
        """
        List all available backup files with metadata

        Args:
            include_failed: Whether to include failed backups in the list

        Returns:
            List of backup information dictionaries
        """
        backup_files = list(self.backup_dir.glob("*.sql"))
        
        # Create a mapping of filenames to file objects
        file_map = {f.name: f for f in backup_files}
        
        # Filter and sort backups from the log
        result = []
        for backup_entry in self.backup_log['backups']:
            filename = Path(backup_entry['filename']).name
            if filename in file_map:
                backup_info = BackupInfo.from_dict(backup_entry)
                if include_failed or backup_info.status != BackupStatus.FAILED:
                    result.append({
                        'filename': backup_info.filename,
                        'size': backup_info.size,
                        'timestamp': backup_info.timestamp,
                        'status': backup_info.status.value,
                        'description': backup_info.description
                    })
        
        # Sort by timestamp (newest first)
        result.sort(key=lambda x: x['timestamp'], reverse=True)
        return result

    def get_backup_info(self, backup_file: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific backup file

        Args:
            backup_file: Path to the backup file

        Returns:
            Dictionary with backup information or None if not found
        """
        backup_path = Path(backup_file)
        filename = backup_path.name
        
        for backup_entry in self.backup_log['backups']:
            if Path(backup_entry['filename']).name == filename:
                backup_info = BackupInfo.from_dict(backup_entry)
                return {
                    'filename': backup_info.filename,
                    'size': backup_info.size,
                    'timestamp': backup_info.timestamp,
                    'status': backup_info.status.value,
                    'description': backup_info.description
                }
        return None

    def cleanup_old_backups(self, keep_count: int = 10, 
                           keep_days: Optional[int] = None) -> int:
        """
        Remove old backup files, keeping only the most recent ones

        Args:
            keep_count: Number of recent backups to keep
            keep_days: Number of days to keep backups (optional)

        Returns:
            Number of files deleted
        """
        all_backups = self.list_backups(include_failed=True)
        
        # Filter by age if keep_days is specified
        if keep_days is not None:
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=keep_days)
            recent_backups = [b for b in all_backups if b['timestamp'] > cutoff_date]
        else:
            recent_backups = all_backups
        
        # Keep only the specified count
        if len(recent_backups) > keep_count:
            backups_to_delete = recent_backups[keep_count:]
        else:
            backups_to_delete = []
        
        deleted_count = 0
        for backup_info in backups_to_delete:
            try:
                backup_path = self.backup_dir / Path(backup_info['filename']).name
                if backup_path.exists():
                    backup_path.unlink()
                    self.logger.info(f"Deleted old backup: {backup_path.name}")
                    
                    # Remove from log as well
                    self.backup_log['backups'] = [
                        b for b in self.backup_log['backups'] 
                        if Path(b['filename']).name != backup_path.name
                    ]
                    self._save_backup_log()
                    
                    deleted_count += 1
            except OSError as e:
                self.logger.error(f"Error deleting backup {backup_info['filename']}: {e}")

        self.logger.info(f"Cleanup completed. Deleted {deleted_count} old backup files.")
        return deleted_count

    def validate_connection(self) -> bool:
        """
        Validate that we can connect to the PostgreSQL database

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_config['password']
            
            cmd = [
                'psql',
                '-h', self.db_config['host'],
                '-p', str(self.db_config['port']),
                '-U', self.db_config['user'],
                '-d', self.db_config['database'],
                '-c', 'SELECT 1;'
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Database connection validation failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Database connection validation error: {e}")
            return False


# Example usage
if __name__ == "__main__":
    # Example configuration
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'train_station_db',
        'user': 'postgres',
        'password': 'postgres'
    }

    backup_manager = EnhancedPostgreSQLBackupManager(db_config)

    # Example: Create a backup
    # backup_file = backup_manager.create_backup("manual_backup", description="Manual backup for testing")

    # Example: List all backups
    # backups = backup_manager.list_backups()
    # print("Available backups:", backups)

    # Example: Get info about a specific backup
    # if backups:
    #     info = backup_manager.get_backup_info(backups[0]['filename'])
    #     print("Backup info:", info)

    # Example: Restore from latest backup
    # if backups:
    #     success = backup_manager.restore_backup(backups[0]['filename'])
    #     print("Restore successful:", success)

    # Example: Cleanup old backups
    # deleted = backup_manager.cleanup_old_backups(keep_count=5)