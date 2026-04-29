import sys
sys.path.insert(0, '/mnt/c/VS_Code/RWSDBv2.1/backend')

print(f"psycopg3_available (before imports): check")

try:
    import psycopg
    from psycopg import sql
    psycopg3_available = True
    print("psycopg3 is available")
except ImportError:
    try:
        import psycopg2
        from psycopg2 import sql
        psycopg3_available = False
        print("psycopg2 is available")
    except ImportError:
        sql = None
        print("No psycopg library")

print(f"psycopg3_available = {psycopg3_available}")