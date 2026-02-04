"""
PostgreSQL Backup Manager for Train Station DBMS
Provides backup and restore functionality for PostgreSQL database
"""

import os
import subprocess
import datetime
import json
from pathlib import Path
from typing import Optional, Dict, Any


class PostgreSQLBackupManager:
    def __init__(self, db_config: Dict[str, Any]):
        """
        Initialize the PostgreSQL backup manager
        
        Args:
            db_config: Dictionary containing database configuration
                      Expected keys: host, port, database, user, password
        """
        self.db_config = db_config
        self.backup_dir = Path('./backups/postgres')
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """
        Create a backup of the PostgreSQL database
        
        Args:
            backup_name: Optional custom name for the backup
            
        Returns:
            Path to the created backup file
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if backup_name:
            filename = f"{backup_name}_{timestamp}.sql"
        else:
            filename = f"{self.db_config['database']}_backup_{timestamp}.sql"
        
        backup_path = self.backup_dir / filename
        
        # Prepare pg_dump command
        cmd = [
            'pg_dump',
            '-h', self.db_config['host'],
            '-p', str(self.db_config['port']),
            '-U', self.db_config['user'],
            '-d', self.db_config['database'],
            '--verbose',
            '--clean',
            '--no-owner',
            '--no-privileges',
            '--file', str(backup_path)
        ]
        
        # Set environment variable for password
        env = os.environ.copy()
        env['PGPASSWORD'] = self.db_config['password']
        
        try:
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
            print(f"Backup created successfully: {backup_path}")
            print(f"Backup size: {backup_path.stat().st_size} bytes")
            return str(backup_path)
        except subprocess.CalledProcessError as e:
            print(f"Backup failed: {e}")
            print(f"Error output: {e.stderr}")
            raise
        except FileNotFoundError:
            print("Error: pg_dump command not found. Please ensure PostgreSQL is installed and in PATH.")
            raise
    
    def restore_backup(self, backup_file: str) -> bool:
        """
        Restore the PostgreSQL database from a backup file
        
        Args:
            backup_file: Path to the backup file to restore from
            
        Returns:
            True if restore was successful, False otherwise
        """
        backup_path = Path(backup_file)
        if not backup_path.exists():
            print(f"Error: Backup file does not exist: {backup_file}")
            return False
        
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
        
        # Set environment variable for password
        env = os.environ.copy()
        env['PGPASSWORD'] = self.db_config['password']
        
        try:
            # Drop the database
            result = subprocess.run(drop_cmd, env=env, capture_output=True, text=True, check=True)
            print("Existing database dropped successfully")
            
            # Recreate the database
            result = subprocess.run(create_cmd, env=env, capture_output=True, text=True, check=True)
            print("New database created successfully")
            
            # Restore from backup
            restore_cmd = [
                'psql',
                '-h', self.db_config['host'],
                '-p', str(self.db_config['port']),
                '-U', self.db_config['user'],
                '-d', self.db_config['database'],
                '-f', str(backup_path)
            ]
            
            result = subprocess.run(restore_cmd, env=env, capture_output=True, text=True, check=True)
            print(f"Database restored successfully from: {backup_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Restore failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
        except FileNotFoundError:
            print("Error: psql command not found. Please ensure PostgreSQL is installed and in PATH.")
            return False
    
    def list_backups(self) -> list:
        """
        List all available backup files
        
        Returns:
            List of backup file paths
        """
        backup_files = list(self.backup_dir.glob("*.sql"))
        return [str(f) for f in sorted(backup_files, key=os.path.getmtime, reverse=True)]
    
    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """
        Remove old backup files, keeping only the most recent ones
        
        Args:
            keep_count: Number of recent backups to keep
            
        Returns:
            Number of files deleted
        """
        backup_files = sorted(self.backup_dir.glob("*.sql"), key=os.path.getmtime, reverse=True)
        files_to_delete = backup_files[keep_count:]
        
        deleted_count = 0
        for file_path in files_to_delete:
            try:
                file_path.unlink()
                print(f"Deleted old backup: {file_path.name}")
                deleted_count += 1
            except OSError as e:
                print(f"Error deleting backup {file_path.name}: {e}")
        
        print(f"Cleanup completed. Deleted {deleted_count} old backup files.")
        return deleted_count


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
    
    backup_manager = PostgreSQLBackupManager(db_config)
    
    # Example: Create a backup
    # backup_file = backup_manager.create_backup("manual_backup")
    
    # Example: List all backups
    # backups = backup_manager.list_backups()
    # print("Available backups:", backups)
    
    # Example: Restore from latest backup
    # if backups:
    #     success = backup_manager.restore_backup(backups[0])
    #     print("Restore successful:", success)
    
    # Example: Cleanup old backups
    # deleted = backup_manager.cleanup_old_backups(keep_count=5)