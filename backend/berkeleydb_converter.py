"""
BerkeleyDB Converter Module
Converts PostgreSQL tables to BerkeleyDB format

This module can be used:
1. As a standalone script: python berkeleydb_converter.py
2. As an API endpoint: POST /api/lab3-convert
3. As an importable module: from berkeleydb_converter import BerkeleyDBConverter

Note: BerkeleyDB libraries (berkeleydb/bsddb3) have limited Windows support.
      As fallback, this converter can export to JSON format.

RWSDBv2.3 - Railway Station Database System
"""

import json
import os
import sys
import logging
import decimal

# Try psycopg 3 first, fall back to psycopg2
psycopg3_available = False
try:
    import psycopg
    from psycopg import sql
    psycopg3_available = True
    logger = logging.getLogger(__name__)
    logger.info("Using psycopg (psycopg3)")
except ImportError:
    try:
        import psycopg2
        from psycopg2 import sql
        logger = logging.getLogger(__name__)
        logger.info("Using psycopg2")
    except ImportError:
        logger = logging.getLogger(__name__)
        logger.error("Neither psycopg nor psycopg2 is installed. Cannot connect to PostgreSQL.")
        sys.exit(1) # Exit if no PostgreSQL driver

# Try to import berkeleydb, fall back to bsddb3, then to JSON-only mode
berkeleydb_available = False
try:
    from berkeleydb import db
    berkeleydb_available = True
    logger = logging.getLogger(__name__)
    logger.info("Using berkeleydb library")
except ImportError:
    try:
        import bsddb3 as db
        berkeleydb_available = True
        logger = logging.getLogger(__name__)
        logger.info("Using bsddb3 library")
    except ImportError:
        logger = logging.getLogger(__name__)
        logger.warning("Neither berkeleydb nor bsddb3 is installed. Will use JSON export mode.")
        logger.warning("Install with: pip install berkeleydb")
        # Create dummy db module for fallback
        db = None


class BerkeleyDBConverter:
    """Converts PostgreSQL tables to BerkeleyDB format"""
    
    def __init__(self, pg_config, output_dir='berkeleydb'):
        """
        Initialize converter
        
        Args:
            pg_config: PostgreSQL connection configuration dict
            output_dir: Directory to store BerkeleyDB files
        """
        self.pg_config = pg_config
        self.output_dir = output_dir
        self.pg_conn = None
        self.bdb_env = None
        
        # Primary key mappings for each table
        self.primary_keys = {
            'passenger': 'passenger_number',
            'train': 'train_number',
            'platform': 'platform_number',
            'ticket': 'ticket_number',
            'schedule': 'schedule_number',
            'employee': 'employee_number',
            'service': 'service_number',
            'appointment': ['employee_number', 'service_number'],
            'work': ['train_number', 'employee_number']
        }
        
        # Tables to convert (Railway Station Database schema)
        self.tables = [
            'passenger',
            'train', 
            'platform',
            'ticket',
            'schedule',
            'employee',
            'service',
            'appointment',
            'work'
        ]
        
    def connect_postgresql(self):
        """Connect to PostgreSQL database"""
        try:
            db_name = self.pg_config.get('database', 'railway_station')
            pg_host = self.pg_config.get('host', 'localhost')
            
            # Detect if running on WSL
            is_wsl = False
            try:
                with open('/proc/version', 'r') as f:
                    is_wsl = 'microsoft' in f.read().lower()
            except FileNotFoundError:
                pass

            # Always use TCP connection with host
            if psycopg3_available:
                self.pg_conn = psycopg.connect(
                    host=pg_host,
                    dbname=db_name,
                    user=self.pg_config.get('user', 'postgres'),
                    password=self.pg_config.get('password', 'postgres'),
                    port=self.pg_config.get('port', 5432)
                )
            else:
                self.pg_conn = psycopg2.connect(
                    host=pg_host,
                    database=db_name,
                    user=self.pg_config.get('user', 'postgres'),
                    password=self.pg_config.get('password', 'postgres'),
                    port=self.pg_config.get('port', 5432)
                )
            logger.info(f"✓ Connected to PostgreSQL: {db_name}")
            return True
        except Exception as e:
            logger.error(f"✗ PostgreSQL connection error: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def disconnect_postgresql(self):
        """Disconnect from PostgreSQL"""
        if self.pg_conn:
            self.pg_conn.close()
            logger.info("✓ Disconnected from PostgreSQL")

    def init_berkeleydb_env(self):
        """Initialize BerkeleyDB environment or fallback to JSON export"""
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"✓ Created output directory: {self.output_dir}")

        if berkeleydb_available:
            # bsddb3 uses hashopen/rnopen directly - no environment needed
            # Store the flag for use in convert_table
            logger.info(f"✓ Using bsddb3 for BerkeleyDB format")
        else:
            # Fallback: use JSON export mode
            logger.info(f"✓ Using JSON export mode (BerkeleyDB not available)")

    def close_berkeleydb_env(self):
        """Close BerkeleyDB environment - no-op with bsddb3 hashopen"""
        # bsddb3 doesn't need explicit environment close
        logger.info("✓ BerkeleyDB conversion completed")
    def get_table_columns(self, table_name):
        """Get column names for a table"""
        cursor = self.pg_conn.cursor()
        query = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = %s 
            AND table_schema = 'public'
            ORDER BY ordinal_position
        """
        cursor.execute(query, (table_name,))
        columns = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return columns
    
    def get_table_data(self, table_name):
        """Get all data from a table"""
        cursor = self.pg_conn.cursor()
        columns = self.get_table_columns(table_name)
        columns_str = ', '.join([f'"{c}"' for c in columns])
        
        query = sql.SQL("SELECT {columns} FROM {table}").format(
            columns=sql.SQL(columns_str),
            table=sql.Identifier(table_name)
        )
        cursor.execute(query)
        
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()
        
        # Convert to list of dicts
        result = []
        for row in rows:
            row_dict = {}
            for i, col in enumerate(column_names):
                value = row[i]
                # Handle special types
                if hasattr(value, 'isoformat'):  # datetime/date
                    value = value.isoformat()
                elif isinstance(value, decimal.Decimal):
                    value = float(value)
                row_dict[col] = value
            result.append(row_dict)
        
        return result
    
    def create_composite_key(self, row, key_columns):
        """Create composite key from multiple columns"""
        key_parts = [str(row[col]) for col in key_columns]
        return '_'.join(key_parts)
    
    def convert_table(self, table_name):
        """Convert a single PostgreSQL table to BerkeleyDB or JSON"""
        logger.info(f"\n{'='*50}")
        logger.info(f"Converting table: {table_name}")
        logger.info(f"{'='*50}")

        # Get primary key(s) for this table
        pk_columns = self.primary_keys.get(table_name, 'id')
        if not isinstance(pk_columns, list):
            pk_columns = [pk_columns]

        # Get table data
        data = self.get_table_data(table_name)
        logger.info(f"  Found {len(data)} records")

        if not data:
            logger.warning(f"  ⚠ No data to convert")
            return 0

        # Insert records
        records_converted = 0
        
        if berkeleydb_available:
            # Create BerkeleyDB database using hashopen
            db_path = os.path.join(self.output_dir, f"{table_name}.db")
            bdb = db.hashopen(db_path, 'c')

            for row in data:
                # Create key
                if len(pk_columns) > 1:
                    key = self.create_composite_key(row, pk_columns)
                else:
                    key = str(row[pk_columns[0]])

                # Serialize value to JSON
                value_json = json.dumps(row, ensure_ascii=False, default=str)

                # Store in BerkeleyDB (use bytes for key and value)
                bdb[key.encode('utf-8')] = value_json.encode('utf-8')
                records_converted += 1

            # Sync and close database
            bdb.sync()
            bdb.close()
            logger.info(f"  ✓ Converted {records_converted} records to {table_name}.db")
        else:
            # Fallback: export to JSON file
            json_path = os.path.join(self.output_dir, f"{table_name}.json")
            
            # Convert data to dict with primary key as key
            export_data = {}
            for row in data:
                if len(pk_columns) > 1:
                    key = self.create_composite_key(row, pk_columns)
                else:
                    key = str(row[pk_columns[0]])
                export_data[key] = row
                records_converted += 1
            
            # Write JSON file
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"  ✓ Exported {records_converted} records to {table_name}.json")
        
        return records_converted
    def convert_all_tables(self):
        """Convert all PostgreSQL tables to BerkeleyDB or JSON"""
        total_records = 0
        tables_converted = 0

        format_name = "BerkeleyDB" if berkeleydb_available else "JSON"
        logger.info("\n" + "="*60)
        logger.info(f"{format_name} Converter - RWSDBv2.3")
        logger.info("="*60)
        logger.info(f"Output directory: {self.output_dir}")
        logger.info(f"Tables to convert: {len(self.tables)}")
        logger.info(f"Format: {format_name}")
        logger.info("="*60)

        for table_name in self.tables:
            try:
                records = self.convert_table(table_name)
                total_records += records
                if records > 0:
                    tables_converted += 1
            except Exception as e:
                logger.error(f"  ✗ Error converting {table_name}: {e}")

        logger.info("\n" + "="*60)
        logger.info("CONVERSION COMPLETE")
        logger.info("="*60)
        logger.info(f"Tables converted: {tables_converted}/{len(self.tables)}")
        logger.info(f"Total records: {total_records}")
        logger.info(f"Output location: {os.path.abspath(self.output_dir)}")
        logger.info("="*60)

        return {
            'tables_converted': tables_converted,
            'total_records': total_records,
            'output_dir': os.path.abspath(self.output_dir)
        }

    def run(self):
        """Run the full conversion process"""
        success = False

        try:
            # Step 1: Connect to PostgreSQL
            if not self.connect_postgresql():
                return {'error': 'Failed to connect to PostgreSQL'}

            # Step 2: Initialize BerkeleyDB environment
            self.init_berkeleydb_env()

            # Step 3: Convert all tables
            result = self.convert_all_tables()
            success = True

            return result

        except Exception as e:
            logger.error(f"\n✗ Conversion failed: {e}")
            return {'error': str(e)}

        finally:
            # Step 4: Cleanup
            self.close_berkeleydb_env()
            self.disconnect_postgresql()

def main():
    """Main entry point"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    
    # PostgreSQL configuration
    pg_config = {
        'host': '172.25.208.1',
        'database': 'railway_station',
        'user': 'postgres',
        'password': 'postgres',
        'port': 5432
    }
    
    # Output directory for BerkeleyDB files
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'berkeleydb')
    
    # Run converter
    converter = BerkeleyDBConverter(pg_config, output_dir)
    result = converter.run()
    
    # Exit with appropriate code
    if 'error' in result:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
