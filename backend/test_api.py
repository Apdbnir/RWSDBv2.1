import json
import urllib.request

# Test login
req = urllib.request.Request(
    'http://localhost:8081/api/login',
    data=json.dumps({'password': '4444'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
try:
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode())
except Exception as e:
    print(f"Error: {e}")

# Test config
with urllib.request.urlopen('http://localhost:8081/api/config') as resp:
    print(resp.read().decode())