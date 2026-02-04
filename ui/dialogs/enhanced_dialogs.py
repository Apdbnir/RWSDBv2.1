"""
Enhanced date input widgets with future date restrictions
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QTimeEdit,
                             QSpinBox, QDoubleSpinBox, QCheckBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtCore import QDate
import re


class EnhancedDateEdit(QDateEdit):
    """
    Enhanced QDateEdit that restricts date selection to current date or past dates only.
    """
    def __init__(self):
        super().__init__()
        self.setCalendarPopup(True)
        # Set maximum date to today
        current_date = QDate.currentDate()
        self.setMaximumDate(current_date)
        self.setDate(current_date)


class AddEntityDialog(QDialog):
    def __init__(self, parent, table_name, columns_info):
        super().__init__(parent)
        self.setWindowTitle(f"Add Record to {table_name}")
        self.setModal(True)
        self.table_name = table_name
        self.columns_info = columns_info
        self.values = {}

        layout = QVBoxLayout()

        # Create input fields for each column except auto-increment primary keys
        self.input_fields = {}
        self.widgets = {}  # Store references to both the input widgets and their validation info
        for col in columns_info:
            if col['primary_key'] and col['type'].upper() in ['INTEGER'] and col['default'] is None:
                # Skip auto-increment primary keys
                continue

            label = QLabel(f"{col['name']} ({col['type']})")
            widget = self.create_input_widget(col)

            # Store both the widget and column info for validation
            self.widgets[col['name']] = {
                'widget': widget,
                'column_info': col,
                'label': label
            }

            layout.addWidget(label)
            layout.addWidget(widget)

        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.setObjectName("ok")  # Green on hover for OK
        ok_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancel")  # Red on hover for cancel
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def create_input_widget(self, col):
        """Create appropriate input widget based on column type"""
        col_type = col['type'].upper()

        # Check if this is a boolean type
        if 'BOOL' in col_type or 'BOOLEAN' in col_type:
            checkbox = QCheckBox("Check if true")
            return checkbox

        # Check if this is a date/datetime type
        if 'DATE' in col_type:
            # Use enhanced date edit that restricts future dates
            date_edit = EnhancedDateEdit()
            return date_edit

        if 'TIME' in col_type:
            time_edit = QTimeEdit()
            return time_edit

        # Check if this is an integer type
        if 'INT' in col_type or 'TINYINT' in col_type or 'SMALLINT' in col_type or 'BIGINT' in col_type:
            spin_box = QSpinBox()
            spin_box.setRange(-2147483648, 2147483647)  # Standard 32-bit integer range
            spin_box.setValue(0)
            return spin_box

        # Check if this is a floating-point type
        if 'REAL' in col_type or 'DOUBLE' in col_type or 'FLOAT' in col_type or 'DECIMAL' in col_type or 'NUMERIC' in col_type:
            double_spin = QDoubleSpinBox()
            double_spin.setRange(-999999999.99, 999999999.99)
            double_spin.setDecimals(2)
            double_spin.setValue(0.0)
            return double_spin

        # For text types, we might want to restrict certain characters or validate format
        # Text-based input field
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(f"Enter {col['name']}")

        # For specific text types, add validation
        if col_type in ['TEXT', 'VARCHAR', 'NVARCHAR', 'CHAR', 'NCHAR']:
            # For now, just a basic line edit, but we could add more specific validation
            pass

        return line_edit

    def validate_and_accept(self):
        """Validate all inputs before accepting the dialog"""
        errors = []

        for col_name, widget_info in self.widgets.items():
            widget = widget_info['widget']
            col_info = widget_info['column_info']
            col_type = col_info['type'].upper()

            # Get the value from the widget
            value = self.get_widget_value(widget, col_type)

            # Validate the value based on column type
            if value is not None and value != "":
                is_valid, error_msg = self.validate_value(value, col_type, col_info)
                if not is_valid:
                    errors.append(f"{col_name}: {error_msg}")

        if errors:
            # Show validation errors to the user
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Input Validation Error", "\n".join(errors))
            return  # Don't accept the dialog if there are validation errors

        # If all validations pass, accept the dialog
        self.accept()

    def get_widget_value(self, widget, col_type):
        """Get the value from the appropriate widget type"""
        if isinstance(widget, QCheckBox):
            return widget.isChecked()
        elif isinstance(widget, QDateEdit):
            return widget.date().toString("yyyy-MM-dd")
        elif isinstance(widget, QTimeEdit):
            return widget.time().toString("HH:mm:ss")
        elif isinstance(widget, QSpinBox):
            return widget.value()
        elif isinstance(widget, QDoubleSpinBox):
            return widget.value()
        elif isinstance(widget, QComboBox):
            return widget.currentText()
        elif isinstance(widget, QLineEdit):
            return widget.text().strip()
        else:
            return None

    def validate_value(self, value, col_type, col_info):
        """Validate a value based on the column type"""
        col_type = col_type.upper()

        # Handle NULL values - if the column allows NULL and the value is empty
        if value == "" or value is None:
            if col_info.get('not_null', False):  # If column is NOT NULL
                return False, "This field cannot be empty"
            return True, ""

        if 'INT' in col_type or 'TINYINT' in col_type or 'SMALLINT' in col_type or 'BIGINT' in col_type:
            try:
                int(value)
                return True, ""
            except ValueError:
                return False, f"Value must be an integer, got: {value}"

        elif 'REAL' in col_type or 'DOUBLE' in col_type or 'FLOAT' in col_type or 'DECIMAL' in col_type or 'NUMERIC' in col_type:
            try:
                float(value)
                return True, ""
            except ValueError:
                return False, f"Value must be a decimal number, got: {value}"

        elif 'BOOL' in col_type or 'BOOLEAN' in col_type:
            # Handle boolean values - both checkbox and text input
            if isinstance(value, bool):
                return True, ""
            elif str(value).upper() in ['TRUE', 'FALSE', '1', '0', 'YES', 'NO']:
                return True, ""
            else:
                return False, f"Value must be boolean (true/false, yes/no, 1/0), got: {value}"

        elif 'DATE' in col_type:
            # Validate date format (YYYY-MM-DD)
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            if not re.match(date_pattern, str(value)):
                return False, f"Date must be in YYYY-MM-DD format, got: {value}"
            try:
                import datetime
                date_obj = datetime.datetime.strptime(str(value), '%Y-%m-%d')
                # Check if the date is from the future (past or current date is allowed)
                current_date = datetime.datetime.now().date()
                if date_obj.date() > current_date:
                    return False, f"Future dates are not allowed, got: {value}. Please enter a date that is today or in the past."
                return True, ""
            except ValueError:
                return False, f"Invalid date: {value}"

        elif 'DATETIME' in col_type or 'TIMESTAMP' in col_type:
            # Validate datetime format (YYYY-MM-DD HH:MM:SS)
            datetime_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
            if not re.match(datetime_pattern, str(value)):
                return False, f"Datetime must be in YYYY-MM-DD HH:MM:SS format, got: {value}"
            try:
                import datetime
                datetime_obj = datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
                # Check if the datetime is from the future (past or current datetime is allowed)
                current_datetime = datetime.datetime.now()
                if datetime_obj > current_datetime:
                    return False, f"Future datetimes are not allowed, got: {value}. Please enter a datetime that is now or in the past."
                return True, ""
            except ValueError:
                return False, f"Invalid datetime: {value}"

        elif 'TIME' in col_type:
            # Validate time format (HH:MM:SS)
            time_pattern = r'^\d{2}:\d{2}:\d{2}$'
            if not re.match(time_pattern, str(value)):
                return False, f"Time must be in HH:MM:SS format, got: {value}"
            try:
                import datetime
                datetime.datetime.strptime(str(value), '%H:%M:%S')
                return True, ""
            except ValueError:
                return False, f"Invalid time: {value}"

        elif 'CHAR' in col_type or 'TEXT' in col_type or 'VARCHAR' in col_type:
            # Text validation - ensure max length if specified
            # PostgreSQL enforces text length based on column definition
            if col_info.get('not_null', False) and str(value).strip() == "":
                return False, "This field cannot be empty"
            return True, ""

        else:
            # For other types, accept the value
            return True, ""

    def get_values(self):
        """Return a dictionary of column names to validated values from input fields"""
        values = {}
        for col_name, widget_info in self.widgets.items():
            widget = widget_info['widget']
            col_info = widget_info['column_info']
            col_type = col_info['type'].upper()

            # Get the value from the widget
            value = self.get_widget_value(widget, col_type)

            # Only include non-empty values
            if value is not None and value != "":
                values[col_name] = value
        return values


class UpdateEntityDialog(QDialog):
    def __init__(self, parent, table_name, columns_info, where_clause):
        super().__init__(parent)
        self.setWindowTitle(f"Update Record in {table_name}")
        self.setModal(True)
        self.table_name = table_name
        self.columns_info = columns_info
        self.where_clause = where_clause
        self.updates = {}

        layout = QVBoxLayout()

        # Show the where clause
        where_label = QLabel(f"WHERE clause: {where_clause}")
        where_label.setWordWrap(True)
        layout.addWidget(where_label)

        # Create input fields for each column (excluding primary keys for update)
        self.input_fields = {}
        self.widgets = {}  # Store references to both the input widgets and their validation info
        for col in columns_info:
            if col['primary_key']:
                # Skip primary key columns for update
                continue

            label = QLabel(f"{col['name']} ({col['type']})")
            widget = self.create_input_widget(col)

            # Store both the widget and column info for validation
            self.widgets[col['name']] = {
                'widget': widget,
                'column_info': col,
                'label': label
            }

            layout.addWidget(label)
            layout.addWidget(widget)

        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("Update")
        ok_btn.setObjectName("update")  # Blue on hover for update
        ok_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancel")  # Red on hover for cancel
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def create_input_widget(self, col):
        """Create appropriate input widget based on column type (same as AddEntityDialog)"""
        col_type = col['type'].upper()

        # Check if this is a boolean type
        if 'BOOL' in col_type or 'BOOLEAN' in col_type:
            checkbox = QCheckBox("Check if true")
            return checkbox

        # Check if this is a date/datetime type
        if 'DATE' in col_type:
            # Use enhanced date edit that restricts future dates
            date_edit = EnhancedDateEdit()
            return date_edit

        if 'TIME' in col_type:
            time_edit = QTimeEdit()
            return time_edit

        # Check if this is an integer type
        if 'INT' in col_type or 'TINYINT' in col_type or 'SMALLINT' in col_type or 'BIGINT' in col_type:
            spin_box = QSpinBox()
            spin_box.setRange(-2147483648, 2147483647)  # Standard 32-bit integer range
            spin_box.setValue(0)
            return spin_box

        # Check if this is a floating-point type
        if 'REAL' in col_type or 'DOUBLE' in col_type or 'FLOAT' in col_type or 'DECIMAL' in col_type or 'NUMERIC' in col_type:
            double_spin = QDoubleSpinBox()
            double_spin.setRange(-999999999.99, 999999999.99)
            double_spin.setDecimals(2)
            double_spin.setValue(0.0)
            return double_spin

        # For text types, we might want to restrict certain characters or validate format
        # Text-based input field
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(f"Enter new value for {col['name']}")

        # For now, just a basic line edit, but we could add more specific validation
        return line_edit

    def validate_and_accept(self):
        """Validate all inputs before accepting the dialog (same validation logic as AddEntityDialog)"""
        errors = []

        for col_name, widget_info in self.widgets.items():
            widget = widget_info['widget']
            col_info = widget_info['column_info']
            col_type = col_info['type'].upper()

            # Get the value from the widget
            value = self.get_widget_value(widget, col_type)

            # Validate the value based on column type
            if value is not None and value != "":
                is_valid, error_msg = self.validate_value(value, col_type, col_info)
                if not is_valid:
                    errors.append(f"{col_name}: {error_msg}")

        if errors:
            # Show validation errors to the user
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Input Validation Error", "\n".join(errors))
            return  # Don't accept the dialog if there are validation errors

        # If all validations pass, accept the dialog
        self.accept()

    def get_widget_value(self, widget, col_type):
        """Get the value from the appropriate widget type (same as AddEntityDialog)"""
        if isinstance(widget, QCheckBox):
            return widget.isChecked()
        elif isinstance(widget, QDateEdit):
            return widget.date().toString("yyyy-MM-dd")
        elif isinstance(widget, QTimeEdit):
            return widget.time().toString("HH:mm:ss")
        elif isinstance(widget, QSpinBox):
            return widget.value()
        elif isinstance(widget, QDoubleSpinBox):
            return widget.value()
        elif isinstance(widget, QComboBox):
            return widget.currentText()
        elif isinstance(widget, QLineEdit):
            return widget.text().strip()
        else:
            return None

    def validate_value(self, value, col_type, col_info):
        """Validate a value based on the column type (same as AddEntityDialog)"""
        col_type = col_type.upper()

        # Handle NULL values - if the column allows NULL and the value is empty
        if value == "" or value is None:
            if col_info.get('not_null', False):  # If column is NOT NULL
                return False, "This field cannot be empty"
            return True, ""

        if 'INT' in col_type or 'TINYINT' in col_type or 'SMALLINT' in col_type or 'BIGINT' in col_type:
            try:
                int(value)
                return True, ""
            except ValueError:
                return False, f"Value must be an integer, got: {value}"

        elif 'REAL' in col_type or 'DOUBLE' in col_type or 'FLOAT' in col_type or 'DECIMAL' in col_type or 'NUMERIC' in col_type:
            try:
                float(value)
                return True, ""
            except ValueError:
                return False, f"Value must be a decimal number, got: {value}"

        elif 'BOOL' in col_type or 'BOOLEAN' in col_type:
            # Handle boolean values - both checkbox and text input
            if isinstance(value, bool):
                return True, ""
            elif str(value).upper() in ['TRUE', 'FALSE', '1', '0', 'YES', 'NO']:
                return True, ""
            else:
                return False, f"Value must be boolean (true/false, yes/no, 1/0), got: {value}"

        elif 'DATE' in col_type:
            # Validate date format (YYYY-MM-DD)
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            if not re.match(date_pattern, str(value)):
                return False, f"Date must be in YYYY-MM-DD format, got: {value}"
            try:
                import datetime
                date_obj = datetime.datetime.strptime(str(value), '%Y-%m-%d')
                # Check if the date is from the future (past or current date is allowed)
                current_date = datetime.datetime.now().date()
                if date_obj.date() > current_date:
                    return False, f"Future dates are not allowed, got: {value}. Please enter a date that is today or in the past."
                return True, ""
            except ValueError:
                return False, f"Invalid date: {value}"

        elif 'DATETIME' in col_type or 'TIMESTAMP' in col_type:
            # Validate datetime format (YYYY-MM-DD HH:MM:SS)
            datetime_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
            if not re.match(datetime_pattern, str(value)):
                return False, f"Datetime must be in YYYY-MM-DD HH:MM:SS format, got: {value}"
            try:
                import datetime
                datetime_obj = datetime.datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
                # Check if the datetime is from the future (past or current datetime is allowed)
                current_datetime = datetime.datetime.now()
                if datetime_obj > current_datetime:
                    return False, f"Future datetimes are not allowed, got: {value}. Please enter a datetime that is now or in the past."
                return True, ""
            except ValueError:
                return False, f"Invalid datetime: {value}"

        elif 'TIME' in col_type:
            # Validate time format (HH:MM:SS)
            time_pattern = r'^\d{2}:\d{2}:\d{2}$'
            if not re.match(time_pattern, str(value)):
                return False, f"Time must be in HH:MM:SS format, got: {value}"
            try:
                import datetime
                datetime.datetime.strptime(str(value), '%H:%M:%S')
                return True, ""
            except ValueError:
                return False, f"Invalid time: {value}"

        elif 'CHAR' in col_type or 'TEXT' in col_type or 'VARCHAR' in col_type:
            # Text validation - ensure max length if specified
            # PostgreSQL enforces text length based on column definition
            if col_info.get('not_null', False) and str(value).strip() == "":
                return False, "This field cannot be empty"
            return True, ""

        else:
            # For other types, accept the value
            return True, ""

    def get_updates(self):
        """Return a dictionary of column names to new validated values from input fields"""
        updates = {}
        for col_name, widget_info in self.widgets.items():
            widget = widget_info['widget']
            col_info = widget_info['column_info']
            col_type = col_info['type'].upper()

            # Get the value from the widget
            value = self.get_widget_value(widget, col_type)

            # Only include non-empty values
            if value is not None and value != "":
                # Only include fields with non-empty values
                updates[col_name] = value
        return updates