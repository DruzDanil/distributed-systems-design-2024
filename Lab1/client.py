import requests


# Відправка POST запиту
data = "Hello World"
response_post = requests.post('http://127.0.0.1:5000/data', data=data)
print('POST відповідь:', response_post.text)

# Відправка GET запиту
response_get = requests.get('http://127.0.0.1:5000/data')
print('GET відповідь:', response_get.json())
