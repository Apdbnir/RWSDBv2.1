import requests
import json

# Login first
login_resp = requests.post(
    'http://localhost:6767/api/login',
    json={'password': '4444'}
)
print("Login:", login_resp.json())

# Get cookie
cookies = login_resp.cookies

# Try insert
data = {
    "train_number": 99,
    "speed": 100,
    "year_of_manufacture": 2020,
    "type": "Test",
    "number_of_cars": 5
}

try:
    insert_resp = requests.post(
        'http://localhost:6767/api/train',
        json=data,
        cookies=cookies
    )
    print("Insert:", insert_resp.status_code, insert_resp.text)
except Exception as e:
    print("Error:", e)