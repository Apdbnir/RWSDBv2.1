import sys
import bsddb3 as db
import os

test_path = "/tmp/test_db2.db"

if os.path.exists(test_path):
    os.remove(test_path)

try:
    bdb = db.hashopen(test_path, 'c')
    
    # Try different ways to store
    key = "test_key"
    value = '{"name": "test"}'
    
    # Method 1: bytes key/value
    bdb[key.encode('utf-8')] = value.encode('utf-8')
    
    result = bdb.get(key.encode('utf-8'))
    print(f"Method 1 (bytes): {result}")
    
    bdb.sync()
    bdb.close()
    print("Success!")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()