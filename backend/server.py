"""
HTTP Server for RWSDBv2.3 - Railway Station Database System v2.3
Implements RESTful API for database operations using BerkeleyDB and PostgreSQL

Laboratory Work №1 & №3
Variant 18

This server provides:
- RESTful API endpoints for all database tables
- Dynamic switching between PostgreSQL and BerkeleyDB
- User role management (user and superuser)
- Lookup table protection (only superusers can modify)
- Database backup functionality
- Data export to JSON, CSV, and Excel formats
"""

import json
import logging
import logging.handlers
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import hashlib
from datetime import datetime
import threading
import queue
import csv
import io
import decimal

# Try to import BerkeleyDB
try:
    import bsddb3 as bdb
except ImportError:
    try:
        from berkeleydb import db as bdb
    except ImportError:
        bdb = None

# Try to import PostgreSQL drivers
psycopg3_available = False
try:
    import psycopg
    from psycopg import sql
    psycopg3_available = True
except ImportError:
    try:
        import psycopg2
        from psycopg2 import sql
    except ImportError:
        sql = None

# Configure logging with both console and file handlers
def setup_logging():
    """Setup comprehensive logging configuration"""
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Root logger for the application
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Console handler - for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # File handler with rotation - for production
    log_file = os.path.join(log_dir, 'server.log')
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Error log file - separate file for errors
    error_log_file = os.path.join(log_dir, 'error.log')
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    
    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    
    return logging.getLogger(__name__)

logger = setup_logging()


class DatabaseManager:
    """Unified Database Manager supporting BerkeleyDB and PostgreSQL"""

    # Lookup tables that require superuser access for modifications
    LOOKUP_TABLES = {'train', 'platform', 'service', 'employee'}

    # All available API tables
    API_TABLES = {
        'passenger', 'train', 'platform', 'ticket',
        'schedule', 'employee', 'service',
        'appointment', 'work'
    }

    # Primary keys for each table
    PRIMARY_KEYS = {
        'passenger': 'passenger_number',
        'train': 'train_number',
        'platform': 'platform_number',
        'ticket': 'ticket_number',
        'schedule': 'schedule_number',
        'employee': 'employee_number',
        'service': 'service_number',
        'appointment': 'employee_number',
        'work': 'work_number'
    }

    def __init__(self, config):
        self.config = config
        self.db_type = config.get('database_type', 'berkeleydb')
        self.bdb_path = config.get('bdb_path')
        self.pg_config = {
            'host': config.get('pg_host', 'localhost'),
            'database': config.get('pg_database', 'railway_station'),
            'user': config.get('pg_user', 'postgres'),
            'password': config.get('pg_password', 'postgres'),
            'port': config.get('pg_port', 5432)
        }
        
        self.bdb_databases = {}
        self.bdb_databases_raw = {}
        self.pg_conn = None
        self._initialize()

    def _initialize(self):
        if self.db_type == 'berkeleydb':
            self._init_berkeleydb()
        else:
            self._init_postgresql()
        # Auto-sync from PostgreSQL to BerkeleyDB if BDB is empty
        if self._needs_auto_sync():
            logger.info("Auto-syncing data from PostgreSQL to BerkeleyDB")
            self.sync_from_postgresql()

    def _needs_auto_sync(self):
        """Check if BerkeleyDB needs to be synced from PostgreSQL"""
        if not hasattr(self, 'bdb_databases'):
            return False
        if not self.bdb_databases:
            return False
        try:
            for table_name in self.API_TABLES:
                if table_name in self.bdb_databases:
                    if len(self.bdb_databases[table_name]) > 0:
                        return False
            return True
        except:
            return True

    def _init_berkeleydb(self):
        if not bdb:
            logger.error("BerkeleyDB library not available")
            return False

        try:
            os.makedirs(self.bdb_path, exist_ok=True)
            for table_name in self.API_TABLES:
                db_file = os.path.join(self.bdb_path, f"{table_name}.db")
                try:
                    table_db = bdb.hashopen(db_file, 'c')
                    self.bdb_databases_raw[table_name] = table_db
                    self.bdb_databases[table_name] = table_db
                except Exception as e:
                    logger.error(f"Failed to initialize BDB table {table_name}: {e}")
            logger.info(f"BerkeleyDB initialized at {self.bdb_path}")
            return True
        except Exception as e:
            logger.error(f"BerkeleyDB initialization error: {e}")
            return False

    def _init_postgresql(self):
        """Initialize PostgreSQL connection"""
        if not sql:
            logger.error("PostgreSQL driver not available")
            return False

        try:
            if psycopg3_available:
                self.pg_conn = psycopg.connect(**self.pg_config)
            else:
                # psycopg2 uses 'database' instead of 'dbname' in some contexts, but connect accepts dbname
                self.pg_conn = psycopg2.connect(
                    host=self.pg_config['host'],
                    dbname=self.pg_config['database'],
                    user=self.pg_config['user'],
                    password=self.pg_config['password'],
                    port=self.pg_config['port']
                )
            self.pg_conn.autocommit = True
            logger.info(f"PostgreSQL connected: {self.pg_config['database']}")
            return True
        except Exception as e:
            logger.error(f"PostgreSQL connection error: {e}")
            return False

    def switch_db(self, new_type):
        """Switch between database types"""
        if new_type == self.db_type:
            return True
        
        logger.info(f"Switching database from {self.db_type} to {new_type}")
        
        # Sync data before switching
        if self.db_type == 'postgresql':
            self.sync_to_berkeleydb()
        
        self.disconnect()
        self.db_type = new_type
        result = self._initialize()
        
        # Sync after switching if going to BerkeleyDB
        if new_type == 'berkeleydb':
            self.sync_from_postgresql()
        
        return result

    def sync_from_postgresql(self):
        """Sync all data from PostgreSQL to BerkeleyDB"""
        if self.db_type != 'berkeleydb':
            return {'error': 'Not in BerkeleyDB mode'}
        if not self.pg_conn:
            return {'error': 'PostgreSQL not connected'}
        
        from berkeleydb_converter import BerkeleyDBConverter
        try:
            converter = BerkeleyDBConverter(self.pg_config, self.bdb_path)
            converter.connect_postgresql()
            result = converter.convert_all_tables()
            return result
        except Exception as e:
            return {'error': str(e)}

    def sync_to_berkeleydb(self):
        """Sync all data from current database to BerkeleyDB"""
        if self.db_type != 'postgresql':
            return {'error': 'Not in PostgreSQL mode'}
        
        from berkeleydb_converter import BerkeleyDBConverter
        try:
            converter = BerkeleyDBConverter(self.pg_config, self.bdb_path)
            converter.connect_postgresql()
            result = converter.convert_all_tables()
            return result
        except Exception as e:
            return {'error': str(e)}

    def disconnect(self):
        """Close all connections"""
        for table_db in self.bdb_databases.values():
            table_db.close()
        self.bdb_databases = {}
        
        if self.pg_conn:
            self.pg_conn.close()
            self.pg_conn = None
        logger.info("Database connections closed")

    def get_primary_key(self, table_name):
        return self.PRIMARY_KEYS.get(table_name, 'id')

    def is_lookup_table(self, table_name):
        return table_name.lower() in self.LOOKUP_TABLES

    def get_table_data(self, table_name, filters=None, limit=None, offset=None):
        if self.db_type == 'berkeleydb':
            return self._get_bdb_data(table_name, filters, limit, offset)
        else:
            return self._get_pg_data(table_name, filters, limit, offset)

    def _get_bdb_data(self, table_name, filters=None, limit=None, offset=None):
        if table_name not in self.bdb_databases:
            return {'error': f'Table {table_name} not found', 'data': [], 'columns': []}

        all_data = []
        db_raw = self.bdb_databases_raw[table_name]
        for key, value in db_raw.items():
            try:
                record = json.loads(value.decode('utf-8'))
                match = True
                if filters:
                    for k, v in filters.items():
                        if str(record.get(k, '')) != str(v):
                            match = False
                            break
                if match:
                    all_data.append(record)
            except:
                continue

        # Sort by primary key for consistency
        pk = self.get_primary_key(table_name)
        all_data.sort(key=lambda x: str(x.get(pk, '')))

        if offset: all_data = all_data[int(offset):]
        if limit: all_data = all_data[:int(limit)]
        
        columns = list(all_data[0].keys()) if all_data else []
        return {'data': all_data, 'columns': columns, 'count': len(all_data)}

    def _get_pg_data(self, table_name, filters=None, limit=None, offset=None):
        if not self.pg_conn: return {'error': 'PG not connected', 'data': [], 'columns': []}
        
        try:
            cursor = self.pg_conn.cursor()
            query = f'SELECT * FROM "{table_name}"'
            params = []
            if filters:
                where_clauses = [f'"{k}" = %s' for k in filters.keys()]
                query += " WHERE " + " AND ".join(where_clauses)
                params.extend(filters.values())
            
            query += f' ORDER BY "{self.get_primary_key(table_name)}"'
            
            if limit: query += f" LIMIT {int(limit)}"
            if offset: query += f" OFFSET {int(offset)}"
            
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            data = []
            for row in rows:
                record = {}
                for i, col in enumerate(columns):
                    val = row[i]
                    if isinstance(val, (datetime, decimal.Decimal)): val = str(val)
                    record[col] = val
                data.append(record)
            
            cursor.close()
            return {'data': data, 'columns': columns, 'count': len(data)}
        except Exception as e:
            return {'error': str(e), 'data': [], 'columns': []}

    def insert_record(self, table_name, data, is_superuser=False):
        if self.is_lookup_table(table_name) and not is_superuser:
            raise PermissionError("Superuser required for lookup tables")

        if self.db_type == 'berkeleydb':
            result = self._insert_bdb(table_name, data)
            self._sync_to_postgresql(table_name, data, 'insert')
            return result
        else:
            result = self._insert_pg(table_name, data)
            self._sync_to_berkeleydb(table_name)
            return result

    def _sync_to_postgresql(self, table_name, data, action='insert'):
        """Auto-sync to PostgreSQL after BerkeleyDB changes"""
        if not self.pg_conn:
            return
        try:
            if action == 'insert':
                pk = self.get_primary_key(table_name)
                key = str(data.get(pk, ''))
                if not key: return
                cursor = self.pg_conn.cursor()
                cols = ", ".join([f'"{k}"' for k in data.keys()])
                placeholders = ", ".join(["%s"] * len(data))
                query = f'INSERT INTO "{table_name}" ({cols}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
                cursor.execute(query, list(data.values()))
                cursor.close()
            self.pg_conn.commit()
        except Exception as e:
            logger.error(f"Sync to PostgreSQL failed: {e}")

    def _sync_to_berkeleydb(self, table_name):
        """Auto-sync table from PostgreSQL"""
        if self.db_type != 'postgresql': return
        try:
            from berkeleydb_converter import BerkeleyDBConverter
            converter = BerkeleyDBConverter(self.pg_config, self.bdb_path)
            converter.connect_postgresql()
            converter.convert_table(table_name)
        except Exception as e:
            logger.error(f"Sync to BerkeleyDB failed: {e}")

    def _insert_bdb(self, table_name, data):
        db_raw = self.bdb_databases_raw[table_name]
        pk = self.get_primary_key(table_name)
        key = str(data.get(pk, ''))
        if not key: raise ValueError("Primary key missing")
        if key in db_raw: raise ValueError("Record exists")
        db_raw[key] = json.dumps(data)
        return data

    def _insert_pg(self, table_name, data):
        cursor = self.pg_conn.cursor()
        cols = ", ".join([f'"{k}"' for k in data.keys()])
        placeholders = ", ".join(["%s"] * len(data))
        query = f'INSERT INTO "{table_name}" ({cols}) VALUES ({placeholders}) RETURNING *'
        cursor.execute(query, list(data.values()))
        row = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        result = dict(zip(columns, row))
        cursor.close()
        return result

    def update_record(self, table_name, record_id, data, is_superuser=False):
        if self.is_lookup_table(table_name) and not is_superuser:
            raise PermissionError("Superuser required")

        if self.db_type == 'berkeleydb':
            return self._update_bdb(table_name, record_id, data)
        else:
            return self._update_pg(table_name, record_id, data)

    def _update_bdb(self, table_name, record_id, data):
        db_raw = self.bdb_databases_raw[table_name]
        key = str(record_id)
        if key not in db_raw: return None
        record = json.loads(db_raw[key])
        record.update(data)
        db_raw[key] = json.dumps(record)
        return record

    def _update_pg(self, table_name, record_id, data):
        cursor = self.pg_conn.cursor()
        set_clause = ", ".join([f'"{k}" = %s' for k in data.keys()])
        pk = self.get_primary_key(table_name)
        query = f'UPDATE "{table_name}" SET {set_clause} WHERE "{pk}" = %s RETURNING *'
        cursor.execute(query, list(data.values()) + [record_id])
        row = cursor.fetchone()
        if not row: return None
        columns = [desc[0] for desc in cursor.description]
        result = dict(zip(columns, row))
        cursor.close()
        return result

    def delete_record(self, table_name, record_id, is_superuser=False):
        if self.is_lookup_table(table_name) and not is_superuser:
            raise PermissionError("Superuser required")

        if self.db_type == 'berkeleydb':
            db_raw = self.bdb_databases_raw[table_name]
            key = str(record_id)
            if key in db_raw:
                del db_raw[key]
                return True
            return False
        else:
            cursor = self.pg_conn.cursor()
            pk = self.get_primary_key(table_name)
            cursor.execute(f'DELETE FROM "{table_name}" WHERE "{pk}" = %s', [record_id])
            success = cursor.rowcount > 0
            cursor.close()
            return success

    def execute_custom_query(self, query):
        if self.db_type == 'berkeleydb':
            return {'error': 'Custom SQL only supported for PostgreSQL'}
        
        try:
            cursor = self.pg_conn.cursor()
            cursor.execute(query)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                data = [dict(zip(columns, row)) for row in rows]
                return {'data': data, 'columns': columns, 'count': len(data)}
            return {'success': True}
        except Exception as e:
            return {'error': str(e)}

    def get_database_statistics(self):
        stats = []
        for table in self.API_TABLES:
            res = self.get_table_data(table, limit=1)
            stats.append({'table': table, 'count': res.get('count', 0)})
        return {'statistics': stats}

    def create_backup(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, f'backup_{timestamp}.json')
        
        backup_data = {}
        for table in self.API_TABLES:
            backup_data[table] = self.get_table_data(table)['data']
            
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False, default=str)
        return backup_path

    def populate_from_json_files(self, json_dir):
        if self.db_type != 'berkeleydb': return False
        count = 0
        for table in self.API_TABLES:
            path = os.path.join(json_dir, f"{table}.json")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle both list and dict formats
                    items = data if isinstance(data, list) else data.values()
                    for item in items:
                        self._insert_bdb(table, item)
                        count += 1
        return count > 0


class RequestHandler(BaseHTTPRequestHandler):
    db_manager = None
    admin_password_hash = None

    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, PATCH')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def _send_json(self, data, status_code=200):
        self._set_headers(status_code)
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))

    def _authenticate(self):
        auth = self.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '): return False
        token = auth.split(' ')[1]
        return hashlib.sha256(token.encode()).hexdigest() == self.admin_password_hash

    def do_OPTIONS(self): self._set_headers(200)

    def do_GET(self):
        parsed = urlparse(self.path)
        parts = parsed.path.strip('/').split('/')
        
        if parts[0] == 'api':
            if len(parts) == 1:
                self._send_json({'message': 'RWSDB API', 'db_type': self.db_manager.db_type})
            elif parts[1] == 'statistics':
                self._send_json(self.db_manager.get_database_statistics())
            elif parts[1] == 'config':
                self._send_json({'database_type': self.db_manager.db_type})
            elif parts[1] in self.db_manager.API_TABLES:
                query = parse_qs(parsed.query)
                filters = {k: v[0] for k, v in query.items() if k not in ['limit', 'offset']}
                res = self.db_manager.get_table_data(parts[1], filters, query.get('limit', [None])[0], query.get('offset', [None])[0])
                self._send_json(res)
            else:
                self._send_json({'error': 'Not found'}, 404)
        else:
            self._serve_static(parsed.path)

    def _serve_static(self, path):
        root = os.path.join(os.path.dirname(__file__), '..', 'web', 'dist')
        if path == '/' or path == '': path = '/index.html'
        fpath = os.path.join(root, path.lstrip('/'))
        if not os.path.exists(fpath): fpath = os.path.join(root, 'index.html')
        
        try:
            with open(fpath, 'rb') as f:
                content = f.read()
            ctype = 'text/html'
            if fpath.endswith('.js'): ctype = 'application/javascript'
            elif fpath.endswith('.css'): ctype = 'text/css'
            elif fpath.endswith('.svg'): ctype = 'image/svg+xml'
            self._set_headers(200, ctype)
            self.wfile.write(content)
        except:
            self._set_headers(404)

    def do_POST(self):
        parts = self.path.strip('/').split('/')
        if parts[0] != 'api': return self._send_json({'error': 'Invalid'}, 404)
        
        content_len = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(content_len).decode()) if content_len else {}

        if parts[1] == 'login':
            pwd_hash = hashlib.sha256(body.get('password', '').encode()).hexdigest()
            if pwd_hash == self.admin_password_hash:
                self._send_json({'success': True, 'token': body.get('password')})
            else:
                self._send_json({'error': 'Invalid'}, 401)
        elif parts[1] == 'config':
            new_type = body.get('database_type')
            if new_type in ['berkeleydb', 'postgresql']:
                success = self.db_manager.switch_db(new_type)
                self._send_json({'success': success, 'database_type': self.db_manager.db_type})
            else:
                self._send_json({'error': 'Invalid type'}, 400)
        elif parts[1] == 'backup':
            if not self._authenticate(): return self._send_json({'error': 'Auth required'}, 401)
            self._send_json({'path': self.db_manager.create_backup()})
        elif parts[1] == 'custom-query':
            self._send_json(self.db_manager.execute_custom_query(body.get('query')))
        elif parts[1] == 'lab3-convert':
            from berkeleydb_converter import BerkeleyDBConverter
            converter = BerkeleyDBConverter(self.db_manager.pg_config, self.db_manager.bdb_path)
            self._send_json(converter.run())
        elif parts[1] in self.db_manager.API_TABLES:
            if not self._authenticate(): return self._send_json({'error': 'Auth required'}, 401)
            try:
                self._send_json(self.db_manager.insert_record(parts[1], body, True), 201)
            except Exception as e:
                self._send_json({'error': str(e)}, 500)

    def do_PUT(self):
        parts = self.path.strip('/').split('/')
        if len(parts) < 3 or parts[0] != 'api': return self._send_json({'error': 'Invalid'}, 404)
        if not self._authenticate(): return self._send_json({'error': 'Auth required'}, 401)
        
        content_len = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(content_len).decode())
        res = self.db_manager.update_record(parts[1], parts[2], body, True)
        if res: self._send_json(res)
        else: self._send_json({'error': 'Not found'}, 404)

    def do_DELETE(self):
        parts = self.path.strip('/').split('/')
        if len(parts) < 3 or parts[0] != 'api': return self._send_json({'error': 'Invalid'}, 404)
        if not self._authenticate(): return self._send_json({'error': 'Auth required'}, 401)
        
        if self.db_manager.delete_record(parts[1], parts[2], True):
            self._send_json({'success': True})
        else:
            self._send_json({'error': 'Not found'}, 404)

    def do_PATCH(self):
        self.do_POST() # Handle export and other actions via POST logic


def load_config():
    path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'admin_password': '4444', 'database_type': 'berkeleydb'}

DEFAULT_PORT = 8080

def run_server(port=6767):
    config = load_config()
    if 'bdb_path' not in config:
        config['bdb_path'] = os.path.join(os.path.dirname(__file__), '..', 'berkeleydb')
    
    db_manager = DatabaseManager(config)
    RequestHandler.db_manager = db_manager
    RequestHandler.admin_password_hash = hashlib.sha256(config.get('admin_password', '4444').encode()).hexdigest()
    
    server = HTTPServer(('', port), RequestHandler)
    print(f"Server started at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        db_manager.disconnect()
        server.shutdown()

if __name__ == '__main__':
    run_server()
