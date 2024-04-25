from flask import Flask, request, jsonify
import uuid
import requests

app = Flask(__name__)
logging_service_url = 'http://127.0.0.1:5001'
message_service_url = 'http://127.0.0.1:5002'
@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        # Обробка GET запиту
        response1 = requests.get(f'{logging_service_url}/data').text
        response2 = requests.get(f'{message_service_url}/data').text
        return jsonify({'message-service': response2, 'logging-service': response1})
    elif request.method == 'POST':
        # Обробка POST запиту
        msg = request.get_data().decode('utf-8')
        print("value:", msg)
        unique_id = uuid.uuid4()
        print("UID:", unique_id)
        data = {f'{unique_id}': msg}
        print("Data:", data)
        response = requests.post(f'{logging_service_url}/data', json=data)
        print("Response", response.text)
        data = response.text
        return data
    else:
        return 'Непідтримуваний метод запиту'

if __name__ == '__main__':
    app.run(debug=True)
