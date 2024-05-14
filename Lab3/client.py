import requests
import json

# Відправка POST запиту
for i in range(10):
    data = f"msg{i+1}"
    response_post = requests.post('http://127.0.0.1:5000/data', data=data)
    print('POST відповідь:', response_post.text)

# Відправка GET запиту
response_get = requests.get('http://127.0.0.1:5000/data').json()
print('GET відповідь:', json.dumps(response_get, indent=5))
