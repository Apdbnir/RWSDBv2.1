"""
Backup manager for automatic file backup functionality in the database application.
"""
import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class BackupManager:
    """Manages automatic backups of database and configuration files"""
    
    def __init__(self, base_directory: str = "backups"):
        self.base_directory = Path(base_directory)
        self.base_directory.mkdir(exist_ok=True)
        
        # Track files that need backup
        self.files_to_backup = set()
    
    def add_file_for_backup(self, file_path: str):
        """Add a file to be monitored for backups"""
        self.files_to_backup.add(file_path)
    
    def create_backup(self, file_path: str, backup_name: Optional[str] = None) -> str:
        """Create a backup of the specified file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist")
        
        # Create backup directory if it doesn't exist
        backup_dir = self.base_directory / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(exist_ok=True)
        
        # Generate backup name
        if backup_name is None:
            backup_name = f"{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_path.suffix}"
        
        backup_path = backup_dir / backup_name
        shutil.copy2(file_path, backup_path)
        
        # Create metadata file
        metadata = {
            "original_file": str(file_path),
            "backup_path": str(backup_path),
            "timestamp": datetime.now().isoformat(),
            "file_size": file_path.stat().st_size
        }
        
        metadata_path = backup_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return str(backup_path)
    
    def create_auto_backup(self, file_path: str) -> Optional[str]:
        """Create an automatic backup before file modification"""
        file_path = Path(file_path)
        
        if file_path.exists():
            try:
                backup_name = f"auto_{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_path.suffix}"
                return self.create_backup(str(file_path), backup_name)
            except Exception as e:
                print(f"Failed to create auto backup for {file_path}: {e}")
                return None
        return None
    
    def restore_backup(self, backup_path: str, original_path: str) -> bool:
        """Restore a file from backup"""
        try:
            backup_path = Path(backup_path)
            original_path = Path(original_path)
            
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup file {backup_path} does not exist")
            
            # Create directory for original file if it doesn't exist
            original_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(backup_path, original_path)
            return True
        except Exception as e:
            print(f"Failed to restore backup {backup_path} to {original_path}: {e}")
            return False
    
    def get_backups_for_file(self, original_path: str) -> list:
        """Get all available backups for a specific file"""
        original_path = Path(original_path)
        backups = []
        
        for backup_dir in self.base_directory.iterdir():
            if backup_dir.is_dir():
                metadata_path = backup_dir / "metadata.json"
                if metadata_path.exists():
                    try:
                        with open(metadata_path, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            if metadata.get("original_file") == str(original_path):
                                backup_file = backup_dir / Path(metadata["backup_path"]).name
                                backups.append({
                                    "backup_path": str(backup_file),
                                    "timestamp": metadata["timestamp"],
                                    "metadata_path": str(metadata_path)
                                })
                    except Exception:
                        continue
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x["timestamp"], reverse=True)
        return backups
    
    def cleanup_old_backups(self, keep_days: int = 7):
        """Remove backups older than the specified number of days"""
        import time
        
        current_time = time.time()
        cutoff_time = current_time - (keep_days * 24 * 60 * 60)
        
        for backup_dir in self.base_directory.iterdir():
            if backup_dir.is_dir():
                # Check directory modification time
                if backup_dir.stat().st_mtime < cutoff_time:
                    try:
                        shutil.rmtree(backup_dir)
                    except Exception as e:
                        print(f"Failed to remove old backup directory {backup_dir}: {e}")
    
    def get_all_backups(self) -> list:
        """Get list of all backups"""
        backups = []
        
        for backup_dir in self.base_directory.iterdir():
            if backup_dir.is_dir():
                metadata_path = backup_dir / "metadata.json"
                if metadata_path.exists():
                    try:
                        with open(metadata_path, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            backups.append({
                                "original_file": metadata["original_file"],
                                "backup_path": metadata["backup_path"],
                                "timestamp": metadata["timestamp"],
                                "file_size": metadata["file_size"]
                            })
                    except Exception:
                        continue
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x["timestamp"], reverse=True)
        return backups