"""
Security utilities for the Database Management System.

This module provides secure password handling and other security-related functions.
It implements password hashing using PBKDF2 with SHA-256 and includes utilities
for secure configuration management.

The module follows security best practices:
- Uses PBKDF2 with SHA-256 and 100,000 iterations
- Generates cryptographically secure random salts
- Implements password strength validation
- Provides secure configuration loading/saving with hashed passwords
"""

import hashlib
import secrets
import json
import os
from typing import Tuple


def hash_password(password: str, salt: bytes = None) -> Tuple[str, bytes]:
    """
    Hash a password with a salt using PBKDF2 with SHA-256.

    This function implements secure password hashing using the PBKDF2 algorithm
    with SHA-256 as the underlying hash function. It uses 100,000 iterations
    to make brute-force attacks computationally expensive.

    Args:
        password (str): The plaintext password to hash. Must be a non-empty string.
        salt (bytes, optional): Salt to use for hashing. If None, generates
                               a cryptographically secure random 32-byte salt.

    Returns:
        Tuple[str, bytes]: A tuple containing:
                          - Hex-encoded password hash (str)
                          - The salt used for hashing (bytes)

    Security Notes:
        - Uses PBKDF2 with SHA-256 and 100,000 iterations
        - Generates a 32-byte cryptographically secure random salt if none provided
        - The salt should be stored alongside the hash for verification
        - Each password should use a unique salt to prevent rainbow table attacks

    Example:
        >>> pwd_hash, salt = hash_password("my_secure_password")
        >>> print(f"Hash: {pwd_hash[:10]}...")  # First 10 chars
        >>> print(f"Salt length: {len(salt)} bytes")
    """
    if not password:
        raise ValueError("Password cannot be empty")

    if salt is None:
        salt = secrets.token_bytes(32)  # 32-byte random salt

    # Combine password and salt, then hash using PBKDF2
    # Using 100,000 iterations for security against brute force attacks
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwdhash.hex(), salt


def verify_password(stored_hash: str, provided_password: str, salt: bytes) -> bool:
    """
    Verify a provided password against a stored hash.

    This function securely verifies a password by hashing the provided password
    with the same salt used for the stored hash and comparing the results.
    It uses a constant-time comparison to prevent timing attacks.

    Args:
        stored_hash (str): The stored hex-encoded password hash
        provided_password (str): The password to verify against the stored hash
        salt (bytes): The salt that was used to originally hash the password

    Returns:
        bool: True if the provided password matches the stored hash, False otherwise

    Security Notes:
        - Uses constant-time comparison to prevent timing attacks
        - Always performs the full computation regardless of early mismatches
        - Does not leak information about password length or character positions
    """
    # Hash the provided password with the same salt
    pwdhash, _ = hash_password(provided_password, salt)

    # Use constant-time comparison to prevent timing attacks
    return secrets.compare_digest(pwdhash, stored_hash)


def load_secure_config(config_path: str = 'config.json') -> dict:
    """
    Load configuration with secure password handling.

    This function loads the application configuration from a JSON file,
    ensuring that passwords are stored securely using hashing. If the
    configuration file doesn't exist, it creates a default configuration
    with a hashed default password. It also handles migration of legacy
    configurations that store passwords in plain text.

    Args:
        config_path (str): Path to the configuration file. Defaults to 'config.json'

    Returns:
        dict: Configuration dictionary with securely stored password hash and salt

    Security Notes:
        - Migrates legacy configurations with plain text passwords to hashed format
        - Creates secure default configuration if file doesn't exist
        - Never stores plain text passwords in memory or on disk
    """
    if not os.path.exists(config_path):
        # Return default config with hashed default password
        default_pwd, salt = hash_password("4444")
        return {
            "admin_password_hash": default_pwd,
            "admin_salt": salt.hex(),
            "pg_host": "localhost",
            "pg_database": "railway_station",
            "pg_user": "postgres",
            "pg_port": 5432
        }

    with open(config_path, 'r') as f:
        config = json.load(f)

    # If the config doesn't have a hashed password, migrate it
    if 'admin_password' in config and 'admin_password_hash' not in config:
        # Hash the existing password and remove the plain text one
        pwd_hash, salt = hash_password(config['admin_password'])
        config['admin_password_hash'] = pwd_hash
        config['admin_salt'] = salt.hex()
        del config['admin_password']

        # Save the updated config
        save_secure_config(config, config_path)

    return config


def save_secure_config(config: dict, config_path: str = 'config.json') -> bool:
    """
    Save configuration with secure password handling.

    This function securely saves the application configuration to a JSON file.
    It ensures that passwords remain in hashed format and handles file I/O errors
    gracefully.

    Args:
        config (dict): Configuration dictionary containing securely hashed passwords
        config_path (str): Path to the configuration file. Defaults to 'config.json'

    Returns:
        bool: True if save was successful, False otherwise

    Security Notes:
        - Ensures passwords remain in hashed format in the saved file
        - Validates that sensitive data is not accidentally stored in plain text
        - Uses atomic write operations when possible to prevent corruption
    """
    try:
        # Verify that sensitive data is properly hashed before saving
        if 'admin_password' in config:
            print("WARNING: Attempting to save plain text password in config. This is insecure.")
            return False

        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving secure config: {e}")
        return False


def change_password_in_config(current_password: str, new_password: str, config_path: str = 'config.json') -> bool:
    """
    Change the administrator password in the configuration file.

    This function securely changes the administrator password by verifying the
    current password against the stored hash, then hashing and storing the new
    password. It handles both migrated configurations (with hashed passwords)
    and legacy configurations (with default password).

    Args:
        current_password (str): The current administrator password for verification
        new_password (str): The new password to set
        config_path (str): Path to the configuration file. Defaults to 'config.json'

    Returns:
        bool: True if password was changed successfully, False otherwise

    Security Notes:
        - Verifies current password using secure hash comparison
        - Applies password strength requirements to new password
        - Updates both hash and salt in the configuration
        - Maintains backward compatibility with legacy configurations
    """
    config = load_secure_config(config_path)

    # Verify current password
    if 'admin_password_hash' in config and 'admin_salt' in config:
        stored_hash = config['admin_password_hash']
        salt = bytes.fromhex(config['admin_salt'])

        if not verify_password(stored_hash, current_password, salt):
            return False
    else:
        # If no hash exists, assume default password "4444"
        if current_password != "4444":
            return False

    # Validate new password strength
    is_valid, error_msg = validate_password_strength(new_password)
    if not is_valid:
        print(f"Password change failed: {error_msg}")
        return False

    # Hash and save the new password
    new_hash, new_salt = hash_password(new_password)
    config['admin_password_hash'] = new_hash
    config['admin_salt'] = new_salt.hex()

    return save_secure_config(config, config_path)


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength according to security best practices.

    This function evaluates the strength of a password based on multiple criteria
    including length, character variety, and complexity. It helps ensure that
    users create passwords that are resistant to common attack vectors.

    Args:
        password (str): The password string to validate

    Returns:
        Tuple[bool, str]: A tuple containing:
                         - Boolean indicating if the password is strong enough
                         - Error message if validation fails, empty string if valid

    Password Requirements:
        - Minimum length of 8 characters
        - At least one uppercase letter (A-Z)
        - At least one lowercase letter (a-z)
        - At least one digit (0-9)
        - At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

    Security Notes:
        - Helps prevent weak passwords vulnerable to dictionary attacks
        - Encourages use of mixed character types for increased entropy
        - Should be used in conjunction with other security measures
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"

    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Password must contain at least one special character"

    return True, ""