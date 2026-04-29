import urllib.request
import json

# Login
req = urllib.request.Request(
    'http://localhost:6767/api/login',
    data=json.dumps({'password': '4444'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode())
    print("Login:", result)
    token = result.get('token', '4444')

# Insert with auth
req2 = urllib.request.Request(
    'http://localhost:6767/api/train',
    data=json.dumps({
        'train_number': 99,
        'speed': 100,
        'year_of_manufacture': 2020,
        'type': 'TestTrain',
        'number_of_cars': 5
    }).encode('utf-8'),
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    },
    method='POST'
)
try:
    with urllib.request.urlopen(req2) as resp2:
        print("Insert:", resp2.read().decode())
except urllib.error.HTTPError as e:
    print(f"Error: {e.code} - {e.read().decode()}")