import json
import os
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox
from typing import Optional, Dict, Any

from utils.backup.file_backup_manager import BackupManager as FileBackupManager
from utils.backup.action_history import ActionHistory, Action
from utils.backup.postgres_backup_manager import PostgreSQLBackupManager
from utils.backup.enhanced_postgres_backup_manager import EnhancedPostgreSQLBackupManager
from utils.backup.enhanced_backup_manager import EnhancedBackupManager, BackupType


class BackupManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.file_backup_manager = FileBackupManager("backups")
        self.action_history = ActionHistory()
        self.session_start_time = datetime.now()

        # Configuration for auto-backup
        self.auto_backup_enabled = True
        self.backup_before_db_operations = True

        # Enhanced PostgreSQL backup manager for full database backups
        if hasattr(db_manager, 'connection_params'):
            self.pg_backup_manager = EnhancedPostgreSQLBackupManager(db_manager.connection_params)
        else:
            self.pg_backup_manager = None

        # Enhanced backup manager for advanced features
        self.enhanced_backup_manager = EnhancedBackupManager(db_manager)

    def create_backup(self, backup_path, backup_type=BackupType.FULL, compress=True, encrypt=False):
        """
        Create a backup of the database with enhanced options.

        Args:
            backup_path: Path where the backup should be saved
            backup_type: Type of backup to create (full, incremental, etc.)
            compress: Whether to compress the backup
            encrypt: Whether to encrypt the backup

        Returns:
            True if backup was successful, False otherwise
        """
        try:
            # Use the enhanced backup manager for advanced features
            backup_file = self.enhanced_backup_manager.create_backup(
                backup_name=Path(backup_path).stem,
                backup_type=backup_type,
                compress=compress,
                encrypt=encrypt,
                include_schema=True,
                include_data=True
            )

            # Copy to the requested path if different from the generated path
            if backup_file != backup_path:
                import shutil
                shutil.copy2(backup_file, backup_path)

            return True
        except Exception as e:
            print(f"Backup error: {e}")
            return False

    def restore_backup(self, backup_path, verify_checksum=True, decrypt=True, decompress=True):
        """
        Restore the database from a backup file using enhanced functionality.

        Args:
            backup_path: Path to the backup file to restore from
            verify_checksum: Whether to verify the backup checksum before restoring
            decrypt: Whether to decrypt the backup before restoring
            decompress: Whether to decompress the backup before restoring

        Returns:
            True if restore was successful, False otherwise
        """
        try:
            # Use the enhanced backup manager for advanced features
            return self.enhanced_backup_manager.restore_backup(
                backup_file=backup_path,
                verify_checksum=verify_checksum,
                decrypt=decrypt,
                decompress=decompress
            )
        except Exception as e:
            print(f"Restore error: {e}")
            return False

    def backup_database_file(self, db_path: str) -> str:
        """Create a backup of the database file"""
        if self.db_manager and self.db_manager.connection:
            # If we have an active connection, close and reopen to ensure consistency
            self.db_manager.connection.commit()

        backup_path = self.file_backup_manager.create_backup(db_path)
        return backup_path

    def backup_file(self, file_path: str) -> str:
        """Create a backup of any file"""
        return self.file_backup_manager.create_backup(file_path)

    def create_auto_backup(self, file_path: str) -> Optional[str]:
        """Create an automatic backup before file modification"""
        if self.auto_backup_enabled:
            return self.file_backup_manager.create_auto_backup(file_path)
        return None

    def get_backups_for_file(self, original_path: str) -> list:
        """Get all available backups for a specific file"""
        return self.file_backup_manager.get_backups_for_file(original_path)

    def get_all_backups(self) -> list:
        """Get list of all backups"""
        return self.file_backup_manager.get_all_backups()

    def cleanup_old_backups(self, keep_days: int = 7):
        """Remove backups older than the specified number of days"""
        self.file_backup_manager.cleanup_old_backups(keep_days)

    def add_action(self, action: Action):
        """Add an action to the history for undo/redo"""
        self.action_history.add_action(action)

    def can_undo(self) -> bool:
        """Check if we can undo an action"""
        return self.action_history.can_undo()

    def can_redo(self) -> bool:
        """Check if we can redo an action"""
        return self.action_history.can_redo()

    def undo(self) -> bool:
        """Undo the last action"""
        return self.action_history.undo()

    def redo(self) -> bool:
        """Redo the next action"""
        return self.action_history.redo()

    def get_undo_description(self) -> str:
        """Get description of the action that would be undone"""
        return self.action_history.get_undo_description()

    def get_redo_description(self) -> str:
        """Get description of the action that would be redone"""
        return self.action_history.get_redo_description()

    def clear_action_history(self):
        """Clear all actions from history"""
        self.action_history.clear()

    def get_action_history_count(self) -> int:
        """Get the number of actions in history"""
        return self.action_history.get_actions_count()

    def create_db_operation_action(self, operation_name: str,
                                  undo_func: callable,
                                  redo_func: callable,
                                  description: str = ""):
        """Create an action for database operations"""
        action = Action(
            name=operation_name,
            undo_func=undo_func,
            redo_func=redo_func,
            description=description
        )
        self.add_action(action)
        return action

    def backup_before_db_operation(self, db_path: str) -> Optional[str]:
        """Create a backup before a database operation if enabled"""
        if self.backup_before_db_operations:
            return self.create_auto_backup(db_path)
        return None

    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about the current session"""
        return {
            "session_start": self.session_start_time.isoformat(),
            "uptime_seconds": (datetime.now() - self.session_start_time).total_seconds(),
            "action_history_count": self.get_action_history_count(),
            "can_undo": self.can_undo(),
            "can_redo": self.can_redo()
        }