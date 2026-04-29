import requests
import json

# Switch to PostgreSQL
response = requests.post(
    'http://localhost:8080/api/config',
    json={'database_type': 'postgresql'}
)
print(response.text)