import json
import os
from datetime import datetime


class QueryHistoryManager:
    def __init__(self):
        self.queries = []
        self.current_db_path = None
        self.history_dir = 'query_history'
        self.update_callback = None  # Callback function to notify UI when queries change

        # Create history directory if it doesn't exist
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

    def set_database(self, db_path):
        """Set the database path to save/load queries specific to this database"""
        self.current_db_path = db_path
        # Load queries for this specific database
        self.load_queries()

    def get_history_file_path(self):
        """Generate a history file path based on the current database path"""
        if not self.current_db_path:
            # If no database is set, use a default file
            return os.path.join(self.history_dir, 'default_query_history.json')

        # Create a safe filename from the database path
        db_name = os.path.basename(self.current_db_path)
        db_name = db_name.replace('.', '_').replace('\\', '_').replace('/', '_')
        return os.path.join(self.history_dir, f'{db_name}_query_history.json')

    def add_query(self, query, description=""):
        query_entry = {
            'query': query,
            'description': description,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Check if query already exists in history to avoid duplicates
        if not any(q['query'] == query for q in self.queries):
            self.queries.append(query_entry)
            self.save_queries()
            # Notify the UI that queries have been updated
            if self.update_callback:
                self.update_callback()

    def get_queries(self):
        return self.queries

    def load_queries(self):
        history_file = self.get_history_file_path()
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                self.queries = json.load(f)
        except FileNotFoundError:
            self.queries = []

    def save_queries(self):
        history_file = self.get_history_file_path()
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.queries, f, indent=2, default=str)

    def delete_query(self, index):
        """Delete a specific query from history by index"""
        if 0 <= index < len(self.queries):
            del self.queries[index]
            self.save_queries()
            # Notify the UI that queries have been updated
            if self.update_callback:
                self.update_callback()

    def delete_query_by_description(self, description):
        """Delete a specific query from history by its description"""
        for i, query in enumerate(self.queries):
            if query.get('description') == description:
                del self.queries[i]
                self.save_queries()
                # Notify the UI that queries have been updated
                if self.update_callback:
                    self.update_callback()
                return True  # Query found and deleted
        return False  # Query not found

    def get_all_history_files(self):
        """Get a list of all history files in the history directory"""
        files = []
        for file in os.listdir(self.history_dir):
            if file.endswith('.json') and file != 'default_query_history.json':
                files.append(file)
        return files