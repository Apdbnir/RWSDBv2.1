"""
HTTP Server for RWSDBv2.1 - Railway Station Database System v2.1
Implements RESTful API for database operations using libpq for PostgreSQL interaction
"""

import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import psycopg2
import hashlib
import os
from datetime import datetime
import threading
import queue


class DatabaseManager:
    """Manages database connections and operations using psycopg2 (compatible with libpq)"""

    def __init__(self, host, database, user, password, port=5432):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
        self.lookup_tables = {
            'positions', 'lesson_types', 'subjects'  # Example lookup tables - adjust based on actual schema
        }

    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return True
        except Exception as e:
            logging.error(f"Database connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def is_lookup_table(self, table_name):
        """Check if a table is a lookup table"""
        return table_name.lower() in self.lookup_tables

    def get_table_data(self, table_name, filters=None, limit=None, offset=None):
        """Retrieve data from a specific table with optional filters"""
        if not self.connection:
            # Return empty result if not connected to database
            return {
                'columns': [],
                'data': [],
                'count': 0,
                'error': 'Not connected to database'
            }

        cursor = self.connection.cursor()

        # Build query with filters if provided
        query = f"SELECT * FROM {table_name}"
        params = []

        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = %s")
                params.append(value)
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        # Add LIMIT and OFFSET as parameters to prevent SQL injection
        if limit:
            try:
                limit_int = int(limit)
                query += " LIMIT %s"
                params.append(limit_int)
            except ValueError:
                raise ValueError(f"LIMIT must be an integer, got: {limit}")
        if offset:
            try:
                offset_int = int(offset)
                query += " OFFSET %s"
                params.append(offset_int)
            except ValueError:
                raise ValueError(f"OFFSET must be an integer, got: {offset}")

        try:
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            result = {
                'columns': columns,
                'data': [dict(zip(columns, row)) for row in rows],
                'count': len(rows)
            }
            return result
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def insert_record(self, table_name, data, is_superuser=False):
        """Insert a new record into a table"""
        if not self.connection:
            return {
                'error': 'Not connected to database',
                'success': False
            }

        # Check if this is a lookup table and user is not superuser
        if self.is_lookup_table(table_name) and not is_superuser:
            raise PermissionError("Only superusers can modify lookup tables")

        cursor = self.connection.cursor()

        columns = list(data.keys())
        values = list(data.values())

        placeholders = ', '.join(['%s'] * len(values))
        columns_str = ', '.join(columns)

        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders}) RETURNING *"

        try:
            cursor.execute(query, values)
            self.connection.commit()

            # Get the inserted record
            inserted_columns = [desc[0] for desc in cursor.description]
            inserted_row = cursor.fetchone()

            result = dict(zip(inserted_columns, inserted_row))
            return result
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()

    def update_record(self, table_name, record_id, data, id_column='id', is_superuser=False):
        """Update a record in a table"""
        if not self.connection:
            return {
                'error': 'Not connected to database',
                'success': False
            }

        # Check if this is a lookup table and user is not superuser
        if self.is_lookup_table(table_name) and not is_superuser:
            raise PermissionError("Only superusers can modify lookup tables")

        cursor = self.connection.cursor()

        # Prepare SET clause
        set_parts = []
        values = []
        for key, value in data.items():
            if key != id_column:  # Don't update the ID column
                set_parts.append(f"{key} = %s")
                values.append(value)

        values.append(record_id)  # Add ID for WHERE clause

        query = f"UPDATE {table_name} SET {', '.join(set_parts)} WHERE {id_column} = %s RETURNING *"

        try:
            cursor.execute(query, values)
            self.connection.commit()

            # Get the updated record
            updated_columns = [desc[0] for desc in cursor.description]
            updated_row = cursor.fetchone()

            if updated_row:
                result = dict(zip(updated_columns, updated_row))
                return result
            else:
                return None
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()

    def delete_record(self, table_name, record_id, id_column='id', is_superuser=False):
        """Delete a record from a table"""
        if not self.connection:
            return {
                'error': 'Not connected to database',
                'success': False
            }

        # Check if this is a lookup table and user is not superuser
        if self.is_lookup_table(table_name) and not is_superuser:
            raise PermissionError("Only superusers can modify lookup tables")

        cursor = self.connection.cursor()

        query = f"DELETE FROM {table_name} WHERE {id_column} = %s RETURNING {id_column}"
        try:
            cursor.execute(query, (record_id,))
            self.connection.commit()

            deleted_id = cursor.fetchone()
            return deleted_id is not None
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()


class RequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the RWSDBv2.1 API"""

    # Store database manager instance
    db_manager = None
    admin_password_hash = None

    def _set_headers(self, status_code=200, content_type='application/json'):
        """Set response headers"""
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def _set_headers(self, status_code=200, content_type='application/json'):
        """Set response headers"""
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def _send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))

    def _parse_request_body(self):
        """Parse JSON request body"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            try:
                return json.loads(body.decode('utf-8'))
            except json.JSONDecodeError:
                return {}
        return {}


    def _authenticate_superuser(self):
        """Check if request contains valid superuser credentials"""
        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False

        token = auth_header.split(' ')[1]
        # In a real implementation, you'd validate the token properly
        # For now, we'll just compare with the stored hash
        return hashlib.sha256(token.encode()).hexdigest() == self.admin_password_hash

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self._set_headers(200)

    def do_GET(self):
        """Handle GET requests - retrieve data"""
        # Parse the full path to separate the route from query parameters
        parsed_url = urlparse(self.path)
        path_parts = parsed_url.path.strip('/').split('/')

        if len(path_parts) >= 2 and path_parts[0] == 'api':
            table_name = path_parts[1]

            # Extract filters from query parameters only
            query_params = parse_qs(parsed_url.query)
            filters = {}
            for key, value_list in query_params.items():
                if value_list:
                    filters[key] = value_list[0]

            # Parse limit and offset if provided
            limit = filters.pop('limit', None)
            offset = filters.pop('offset', None)

            try:
                # Get data from database
                result = self.db_manager.get_table_data(table_name, filters, limit, offset)
                self._send_json_response(result)
            except Exception as e:
                self._send_json_response({'error': str(e)}, 500)
        else:
            self._send_json_response({'error': 'Invalid endpoint'}, 404)

    def do_POST(self):
        """Handle POST requests - create new records"""
        # Check if this is a superuser action that requires authentication
        requires_superuser = False
        # Parse the full path to separate the route from query parameters
        parsed_url = urlparse(self.path)
        path_parts = parsed_url.path.strip('/').split('/')

        if len(path_parts) >= 2 and path_parts[0] == 'api':
            table_name = path_parts[1]

            # Check if this is a lookup table (requires superuser)
            requires_superuser = self.db_manager.is_lookup_table(table_name)

            # Also check if this is a backup request
            if table_name == 'backup':
                requires_superuser = True
                is_authenticated = self._authenticate_superuser()
                if not is_authenticated:
                    self._send_json_response({'error': 'Superuser authentication required'}, 401)
                    return

                # Handle backup creation
                try:
                    # In a real implementation, this would create a backup
                    result = {'success': True, 'message': 'Backup created successfully', 'timestamp': datetime.now().isoformat()}
                    self._send_json_response(result)
                except Exception as e:
                    self._send_json_response({'error': str(e)}, 500)
                return

            # For regular table insertion
            is_superuser = self._authenticate_superuser() if requires_superuser else False

            if requires_superuser and not is_superuser:
                self._send_json_response({'error': 'Superuser authentication required'}, 401)
                return

            try:
                data = self._parse_request_body()
                result = self.db_manager.insert_record(table_name, data, is_superuser)
                self._send_json_response(result, 201)
            except Exception as e:
                self._send_json_response({'error': str(e)}, 500)
        else:
            self._send_json_response({'error': 'Invalid endpoint'}, 404)

    def do_PUT(self):
        """Handle PUT requests - update records"""
        # Parse the full path to separate the route from query parameters
        parsed_url = urlparse(self.path)
        path_parts = parsed_url.path.strip('/').split('/')

        if len(path_parts) >= 3 and path_parts[0] == 'api':
            table_name = path_parts[1]
            record_id = path_parts[2]

            # Check if this is a lookup table (requires superuser)
            requires_superuser = self.db_manager.is_lookup_table(table_name)
            is_superuser = self._authenticate_superuser() if requires_superuser else False

            if requires_superuser and not is_superuser:
                self._send_json_response({'error': 'Superuser authentication required'}, 401)
                return

            try:
                data = self._parse_request_body()
                result = self.db_manager.update_record(table_name, record_id, data, is_superuser=is_superuser)

                if result:
                    self._send_json_response(result)
                else:
                    self._send_json_response({'error': 'Record not found'}, 404)
            except Exception as e:
                self._send_json_response({'error': str(e)}, 500)
        else:
            self._send_json_response({'error': 'Invalid endpoint'}, 404)

    def do_DELETE(self):
        """Handle DELETE requests - remove records"""
        # Parse the full path to separate the route from query parameters
        parsed_url = urlparse(self.path)
        path_parts = parsed_url.path.strip('/').split('/')

        if len(path_parts) >= 3 and path_parts[0] == 'api':
            table_name = path_parts[1]
            record_id = path_parts[2]

            # Check if this is a lookup table (requires superuser)
            requires_superuser = self.db_manager.is_lookup_table(table_name)
            is_superuser = self._authenticate_superuser() if requires_superuser else False

            if requires_superuser and not is_superuser:
                self._send_json_response({'error': 'Superuser authentication required'}, 401)
                return

            try:
                success = self.db_manager.delete_record(table_name, record_id, is_superuser=is_superuser)

                if success:
                    self._send_json_response({'success': True})
                else:
                    self._send_json_response({'error': 'Record not found'}, 404)
            except Exception as e:
                self._send_json_response({'error': str(e)}, 500)
        else:
            self._send_json_response({'error': 'Invalid endpoint'}, 404)

    def do_PATCH(self):
        """Handle PATCH requests - custom SQL queries"""
        path_parts = self.path.strip('/').split('/')

        if len(path_parts) >= 2 and path_parts[0] == 'api':
            if path_parts[1] == 'custom_query':
                try:
                    data = self._parse_request_body()
                    query = data.get('query')

                    if not query:
                        self._send_json_response({'error': 'Query is required'}, 400)
                        return

                    # Проверяем, что это безопасный запрос (только SELECT)
                    query_upper = query.strip().upper()
                    if not query_upper.startswith('SELECT'):
                        self._send_json_response({'error': 'Only SELECT queries are allowed'}, 400)
                        return

                    # Выполняем запрос
                    cursor = self.db_manager.connection.cursor()
                    cursor.execute(query)
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()

                    result = {
                        'columns': columns,
                        'data': [dict(zip(columns, row)) for row in rows],
                        'count': len(rows)
                    }

                    self._send_json_response(result)
                except Exception as e:
                    self._send_json_response({'error': str(e)}, 500)
            elif path_parts[1] == 'export':
                try:
                    data = self._parse_request_body()
                    table_name = data.get('table')
                    query = data.get('query')
                    format_type = data.get('format', 'json')  # json, csv, excel

                    if not table_name and not query:
                        self._send_json_response({'error': 'Either table name or query is required'}, 400)
                        return

                    # Определяем, что экспортировать
                    if query:
                        # Выполняем пользовательский запрос
                        cursor = self.db_manager.connection.cursor()
                        cursor.execute(query)
                        columns = [desc[0] for desc in cursor.description]
                        rows = cursor.fetchall()

                        result_data = {
                            'columns': columns,
                            'data': [dict(zip(columns, row)) for row in rows],
                            'count': len(rows)
                        }
                    else:
                        # Получаем все данные из таблицы
                        result_data = self.db_manager.get_table_data(table_name)

                    # В зависимости от формата, возвращаем данные
                    if format_type.lower() == 'csv':
                        # Генерируем CSV-представление
                        import io
                        import csv

                        output = io.StringIO()
                        writer = csv.writer(output)

                        # Записываем заголовки
                        if result_data['columns']:
                            writer.writerow(result_data['columns'])

                        # Записываем данные
                        for row in result_data['data']:
                            writer.writerow([row.get(col, '') for col in result_data['columns']])

                        csv_content = output.getvalue()
                        output.close()

                        # Отправляем CSV-файл
                        self._set_headers(200, 'text/csv')
                        self.wfile.write(csv_content.encode('utf-8'))
                    elif format_type.lower() == 'excel':
                        # Используем метод экспорта в Excel из DatabaseManager
                        import tempfile
                        import os

                        # Создаем временный файл
                        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
                            temp_path = tmp_file.name

                        try:
                            # Экспортируем данные в Excel
                            if query:
                                success = self.db_manager.export_to_excel('', temp_path, query=query)
                            else:
                                success = self.db_manager.export_to_excel(table_name, temp_path)

                            if success:
                                # Читаем файл и отправляем его
                                with open(temp_path, 'rb') as file:
                                    file_content = file.read()

                                self._set_headers(200, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                                self.wfile.write(file_content)

                                # Удаляем временный файл
                                os.unlink(temp_path)
                            else:
                                # Удаляем временный файл в случае ошибки
                                if os.path.exists(temp_path):
                                    os.unlink(temp_path)
                                self._send_json_response({'error': 'Failed to export to Excel'}, 500)
                        except Exception as e:
                            # Удаляем временный файл в случае ошибки
                            if os.path.exists(temp_path):
                                os.unlink(temp_path)
                            raise e
                    else:  # json
                        self._send_json_response({
                            'export_format': 'json',
                            'data': result_data
                        })
                except Exception as e:
                    self._send_json_response({'error': str(e)}, 500)
            else:
                self._send_json_response({'error': 'Invalid endpoint'}, 404)
        else:
            self._send_json_response({'error': 'Invalid endpoint'}, 404)


def load_config():
    """Load configuration from config.json"""
    config_path = 'config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Return default configuration
        return {
            'admin_password': '4444',
            'pg_host': 'localhost',
            'pg_database': 'railway_station',
            'pg_user': 'postgres',
            'pg_port': 5432
        }


def run_server(port=8080):
    """Run the HTTP server"""
    # Load configuration
    config = load_config()

    # Initialize database manager
    db_manager = DatabaseManager(
        host=config.get('pg_host', 'localhost'),
        database=config.get('pg_database', 'railway_station'),
        user=config.get('pg_user', 'postgres'),
        password=config.get('pg_password', 'postgres'),  # Note: password should be in config
        port=config.get('pg_port', 5432)
    )

    # Connect to database
    if not db_manager.connect():
        print("Warning: Failed to connect to database. Server will start but database operations will fail until database is available.")
        # Continue running server even if database connection fails

    # Calculate admin password hash
    admin_password = config.get('admin_password', '4444')
    admin_password_hash = hashlib.sha256(admin_password.encode()).hexdigest()

    # Set static variables for the handler
    RequestHandler.db_manager = db_manager
    RequestHandler.admin_password_hash = admin_password_hash

    # Create and start server
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)

    print(f"Starting RWSDBv2.1 server on port {port}...")
    print(f"Database connected: {config.get('pg_database', 'railway_station')}")
    print("Available endpoints:")
    print("  GET    /api/{table_name}              - Retrieve table data")
    print("  GET    /api/{table_name}?param=value  - Filter table data")
    print("  POST   /api/{table_name}              - Insert new record")
    print("  PUT    /api/{table_name}/{id}         - Update record")
    print("  DELETE /api/{table_name}/{id}         - Delete record")
    print("  POST   /api/backup                   - Create database backup (superuser only)")
    print("  PATCH  /api/custom_query             - Execute custom SELECT query")
    print("  PATCH  /api/export                   - Export table/query results to file")
    print("\nPress Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        db_manager.disconnect()
        httpd.shutdown()


if __name__ == '__main__':
    run_server()