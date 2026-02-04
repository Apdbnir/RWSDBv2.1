"""
Utility functions and helpers for RWSDBv2.1
Provides common functionality used throughout the Railway Station Database System v2.1
"""


def format_connection_string(host, port, database, user):
    """Format a PostgreSQL connection string"""
    return f"postgresql://{user}@{host}:{port}/{database}"


def validate_input(data, field_type):
    """Validate input data based on field type"""
    # Validation logic would go here
    return True


def sanitize_input(user_input):
    """Sanitize user input to prevent injection attacks"""
    # Sanitization logic would go here
    return user_input


def log_activity(activity, user, timestamp=None):
    """Log user activity for audit purposes"""
    import datetime
    if timestamp is None:
        timestamp = datetime.datetime.now()
    print(f"[{timestamp}] {user}: {activity}")


def export_to_excel(data, filename):
    """Export data to Excel format"""
    # Excel export logic would go here
    print(f"Exporting {len(data)} records to {filename}")


def backup_database(db_connection, backup_path):
    """Create a backup of the database"""
    # Backup logic would go here
    print(f"Backing up database to {backup_path}")


def restore_database(db_connection, backup_path):
    """Restore database from backup"""
    # Restore logic would go here
    print(f"Restoring database from {backup_path}")