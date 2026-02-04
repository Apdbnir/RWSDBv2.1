"""
Utility functions for exporting query results to various formats
"""
import os
import json
import csv
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import QAbstractTableModel


class ExportUtils:
    def __init__(self, parent_widget):
        self.parent = parent_widget

    def export_to_txt(self, table_widget, title="Query Results"):
        """Export table data to TXT format"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Save as TXT",
            f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not file_path:
            return False

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n")
                f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Write headers
                headers = []
                for col in range(table_widget.columnCount()):
                    header = table_widget.horizontalHeaderItem(col)
                    headers.append(header.text() if header else f"Column {col+1}")
                
                # Write header row
                header_line = " | ".join(headers)
                f.write(header_line + "\n")
                f.write("-" * len(header_line) + "\n")
                
                # Write data rows
                for row in range(table_widget.rowCount()):
                    row_data = []
                    for col in range(table_widget.columnCount()):
                        item = table_widget.item(row, col)
                        value = item.text() if item else ""
                        row_data.append(value)
                    
                    f.write(" | ".join(row_data) + "\n")
            
            QMessageBox.information(self.parent, "Export Successful", 
                                  f"Data exported to {file_path}")
            return True
        except Exception as e:
            QMessageBox.critical(self.parent, "Export Error", 
                               f"Failed to export to TXT: {str(e)}")
            return False

    def export_to_md(self, table_widget, title="Query Results"):
        """Export table data to Markdown format"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Save as Markdown",
            f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            "Markdown Files (*.md);;All Files (*)"
        )
        
        if not file_path:
            return False

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"*Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                
                # Write headers
                headers = []
                for col in range(table_widget.columnCount()):
                    header = table_widget.horizontalHeaderItem(col)
                    headers.append(header.text() if header else f"Column {col+1}")
                
                # Write markdown table header
                f.write("| " + " | ".join(headers) + " |\n")
                f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
                
                # Write data rows
                for row in range(table_widget.rowCount()):
                    row_data = []
                    for col in range(table_widget.columnCount()):
                        item = table_widget.item(row, col)
                        value = item.text() if item else ""
                        row_data.append(value)
                    
                    f.write("| " + " | ".join(row_data) + " |\n")
            
            QMessageBox.information(self.parent, "Export Successful", 
                                  f"Data exported to {file_path}")
            return True
        except Exception as e:
            QMessageBox.critical(self.parent, "Export Error", 
                               f"Failed to export to Markdown: {str(e)}")
            return False


    def export_to_sql(self, table_widget, query, table_name="exported_data"):
        """Export query results to SQL INSERT statements format"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "Save as SQL",
            f"query_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql",
            "SQL Files (*.sql);;All Files (*)"
        )
        
        if not file_path:
            return False

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"-- SQL Export from Query Results\n")
                f.write(f"-- Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"-- Original Query: {query}\n\n")
                
                if table_widget.rowCount() == 0:
                    f.write("-- No data to export\n")
                    QMessageBox.information(self.parent, "Export Successful", 
                                          f"Empty data exported to {file_path}")
                    return True
                
                # Get column headers
                headers = []
                for col in range(table_widget.columnCount()):
                    header = table_widget.horizontalHeaderItem(col)
                    headers.append(header.text() if header else f"column_{col+1}")
                
                # Write CREATE TABLE statement
                f.write(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
                for i, header in enumerate(headers):
                    # Try to determine column type (simplified - defaults to TEXT)
                    f.write(f"    {header} TEXT")
                    if i < len(headers) - 1:
                        f.write(",")
                    f.write("\n")
                f.write(");\n\n")
                
                # Write INSERT statements
                for row in range(table_widget.rowCount()):
                    values = []
                    for col in range(table_widget.columnCount()):
                        item = table_widget.item(row, col)
                        value = item.text() if item else ""
                        # Escape single quotes in values
                        escaped_value = value.replace("'", "''")
                        values.append(f"'{escaped_value}'")
                    
                    f.write(f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(values)});\n")
            
            QMessageBox.information(self.parent, "Export Successful", 
                                  f"Data exported to {file_path}")
            return True
        except Exception as e:
            QMessageBox.critical(self.parent, "Export Error", 
                               f"Failed to export to SQL: {str(e)}")
            return False