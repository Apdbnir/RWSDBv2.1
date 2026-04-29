import sys
sys.path.insert(0, '/mnt/c/VS_Code/RWSDBv2.1/backend')

psycopg3_available = False

try:
    import psycopg
    from psycopg import sql
    psycopg3_available = True
    print("psycopg3 is available")
except ImportError:
    try:
        import psycopg2
        from psycopg2 import sql
        print("psycopg2 is available")
    except ImportError:
        sql = None
        print("No psycopg library")

print(f"psycopg3_available = {psycopg3_available}")

import json

config_path = '/mnt/c/VS_Code/RWSDBv2.1/backend/config.json'
with open(config_path) as f:
    config = json.load(f)

pg_config = {
    'host': config.get('pg_host', 'localhost'),
    'database': config.get('pg_database', 'railway_station'),
    'user': config.get('pg_user', 'postgres'),
    'password': config.get('pg_password', 'postgres'),
    'port': config.get('pg_port', 5432)
}

if psycopg3_available:
    print(f"Using psycopg3, config: {pg_config}")
    conn = psycopg.connect(**pg_config)
else:
    print(f"Using psycopg2, config: {pg_config}")
    conn = psycopg2.connect(
        host=pg_config['host'],
        dbname=pg_config['database'],
        user=pg_config['user'],
        password=pg_config['password'],
        port=pg_config['port']
    )

print(f"Connection: {conn}")
conn.close()