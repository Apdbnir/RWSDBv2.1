"""
Login dialog for admin/user mode selection. Now shows a separate password dialog when admin mode is selected.
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QGroupBox, QMessageBox, QLineEdit,
                             QFormLayout, QInputDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_mode = None  # Will store 'admin' or 'user'
        # Load admin password from configuration file or use default
        self.admin_password = self.load_admin_password()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Login - Database Management System")
        self.setFixedSize(400, 250)  # Reduced size since password field will be in separate dialog

        layout = QVBoxLayout()

        # Title
        title_label = QLabel("Database Management System")
        title_font = QFont("Arial", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel("Please select your access mode:")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Mode selection group
        mode_group = QGroupBox("Access Mode")
        mode_layout = QVBoxLayout()

        # Admin button - will show password dialog when clicked
        self.admin_btn = QPushButton("Administrator Mode")
        self.admin_btn.clicked.connect(self.request_admin_password)
        self.admin_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f1c40f;  /* Yellow on hover */
            }
            QPushButton:pressed {
                background-color: #f39c12;  /* Darker yellow when pressed */
            }
        """)
        mode_layout.addWidget(self.admin_btn)

        # User button
        self.user_btn = QPushButton("User Mode")
        self.user_btn.clicked.connect(self.select_user_mode)
        self.user_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3498db;  /* Blue on hover */
            }
            QPushButton:pressed {
                background-color: #2980b9;  /* Darker blue when pressed */
            }
        """)
        mode_layout.addWidget(self.user_btn)

        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Info text
        info_label = QLabel(
            "Administrator Mode: Full access (requires password)\n"
            "User Mode: Read-only access"
        )
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("color: gray;")
        layout.addWidget(info_label)

        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e74c3c;  /* Red on hover */
            }
            QPushButton:pressed {
                background-color: #c0392b;  /* Darker red when pressed */
            }
        """)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def request_admin_password(self):
        """Request admin password in a separate dialog"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
        from PyQt6.QtCore import Qt

        # Create a custom password dialog to allow for button styling
        dialog = QDialog(self)
        dialog.setWindowTitle("Admin Authentication")
        dialog.setModal(True)
        dialog.setFixedSize(300, 120)  # Adjusted height to accommodate the layout with 0 bottom margin

        layout = QVBoxLayout()
        # Remove bottom margin so buttons are closer to bottom edge
        layout.setContentsMargins(10, 10, 10, 0)  # Left, top, right, bottom margins - bottom set to 0
        layout.setSpacing(0)  # Remove default spacing since we're using spacers

        # Create a horizontal layout for the label and password field on the same line
        h_layout = QHBoxLayout()

        # Left aligned label (without the colon at the end since field will be next to it)
        label = QLabel("Enter Administrator Password:")
        h_layout.addWidget(label)

        # Password field (on the same line as the label, right after the colon)
        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.EchoMode.Password)
        h_layout.addWidget(password_field)

        # Add the horizontal layout to the main vertical layout
        layout.addLayout(h_layout)

        # No additional spacer - let the layout distribute space naturally

        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)  # Set spacing between buttons to 10 pixels

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(dialog.accept)
        ok_btn.setStyleSheet("""
            QPushButton {
                min-width: 80px;
                background-color: #4a4a4a;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;  /* Green on hover */
            }
            QPushButton:pressed {
                background-color: #219653;  /* Darker green when pressed */
            }
        """)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                min-width: 80px;
                background-color: #4a4a4a;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e74c3c;  /* Red on hover */
            }
            QPushButton:pressed {
                background-color: #c0392b;  /* Darker red when pressed */
            }
        """)

        # Add stretch to push buttons to the right
        button_layout.addStretch()
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            password = password_field.text()
            if self.authenticate_admin(password):
                self.user_mode = 'admin'
                self.accept()
            else:
                # Show error message
                QMessageBox.warning(
                    self,
                    "Authentication Failed",
                    "Incorrect password. Please try again."
                )
                # Retry password
                self.request_admin_password()
        # If user cancelled, do nothing - they stay on the login screen

    def authenticate_admin(self, password):
        """Authenticate admin user with password"""
        # Load the admin password hash and salt from config
        import json
        import os
        config_file = 'config.json'

        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)

                # Check if we have hashed password in config
                if 'admin_password_hash' in config and 'admin_salt' in config:
                    stored_hash = config['admin_password_hash']
                    salt = bytes.fromhex(config['admin_salt'])

                    # Use the security module to verify the password
                    from utils.security import verify_password
                    return verify_password(stored_hash, password, salt)
                else:
                    # Fallback to plain text comparison if no hash exists
                    return password == self.admin_password
            except:
                # If there's an error reading the file, fall back to default
                return password == self.admin_password
        else:
            # If no config file exists, use the loaded password
            return password == self.admin_password

    def load_admin_password(self):
        """Load the admin password from a configuration file"""
        import json
        import os
        config_file = 'config.json'

        # Check if the config file exists
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('admin_password', 'admin123')
            except:
                # If there's an error reading the file, return the default password
                return 'admin123'
        else:
            # If no config file exists, return the default password
            return 'admin123'

    def select_user_mode(self):
        """Handle user mode selection"""
        # Create a custom confirmation dialog to allow for specific layout control
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy

        # Create a custom dialog to control margins
        confirm_dialog = QDialog(self)
        confirm_dialog.setWindowTitle("Confirm User Mode")
        confirm_dialog.setModal(True)
        confirm_dialog.setFixedSize(350, 150)

        layout = QVBoxLayout()
        # Set left margin to 10 pixels as requested
        layout.setContentsMargins(10, 10, 10, 10)  # [left, top, right, bottom]
        layout.setSpacing(10)

        # Message label
        label = QLabel("You are selecting User Mode (Read-only access).\n"
                      "You will not be able to modify data in this mode.\n\n"
                      "Continue?")
        label.setWordWrap(True)
        layout.addWidget(label)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Add stretch to push buttons to the right
        button_layout.addStretch()

        # No button
        no_btn = QPushButton("No")
        no_btn.clicked.connect(confirm_dialog.reject)
        no_btn.setStyleSheet("""
            QPushButton {
                min-width: 80px;
                background-color: #4a4a4a;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e74c3c;  /* Red on hover */
            }
            QPushButton:pressed {
                background-color: #c0392b;  /* Darker red when pressed */
            }
        """)

        # Yes button
        yes_btn = QPushButton("Yes")
        yes_btn.clicked.connect(confirm_dialog.accept)  # Connect to accept
        yes_btn.setStyleSheet("""
            QPushButton {
                min-width: 80px;
                background-color: #4a4a4a;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;  /* Green on hover */
            }
            QPushButton:pressed {
                background-color: #219653;  /* Darker green when pressed */
            }
        """)

        button_layout.addWidget(no_btn)
        button_layout.addWidget(yes_btn)

        layout.addLayout(button_layout)
        confirm_dialog.setLayout(layout)

        reply = confirm_dialog.exec()

        if reply == QDialog.DialogCode.Accepted:
            self.user_mode = 'user'
            self.accept()