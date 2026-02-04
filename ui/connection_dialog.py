from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit,
                             QFormLayout, QWidget, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connection_type = 'postgresql'  # PostgreSQL only
        self.connection_params = {}
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("PostgreSQL Database Connection")
        self.setFixedSize(500, 350)

        layout = QVBoxLayout()

        # Title
        title_label = QLabel("PostgreSQL Database Connection")
        title_font = QFont("Arial", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # PostgreSQL connection parameters form
        form_layout = QFormLayout()

        # PostgreSQL connection parameters
        self.pg_host_input = QLineEdit("localhost")
        form_layout.addRow("Host:", self.pg_host_input)

        self.pg_port_input = QLineEdit("5432")
        form_layout.addRow("Port:", self.pg_port_input)

        self.pg_database_input = QLineEdit("train_station_db")
        form_layout.addRow("Database:", self.pg_database_input)

        self.pg_username_input = QLineEdit("postgres")
        form_layout.addRow("Username:", self.pg_username_input)

        self.pg_password_input = QLineEdit()
        self.pg_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Password:", self.pg_password_input)

        self.pg_ssl_checkbox = QCheckBox("Use SSL")
        self.pg_ssl_checkbox.setChecked(False)
        form_layout.addRow("", self.pg_ssl_checkbox)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()

        connect_btn = QPushButton("Connect")
        connect_btn.clicked.connect(self.accept)
        connect_btn.setObjectName("ok")

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setObjectName("cancel")

        button_layout.addWidget(connect_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_connection_info(self):
        """Get the PostgreSQL connection parameters"""
        return {
            'db_type': 'postgresql',
            'connection_params': {
                'host': self.pg_host_input.text(),
                'port': self.pg_port_input.text(),
                'database': self.pg_database_input.text(),
                'user': self.pg_username_input.text(),
                'password': self.pg_password_input.text(),
                'sslmode': 'require' if self.pg_ssl_checkbox.isChecked() else 'prefer'
            }
        }