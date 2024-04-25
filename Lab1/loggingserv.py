from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
facade_server_url = 'http://127.0.0.1:5000'
hash_table = {}

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        # Обробка GET запиту
        print("Hash msg:", list(hash_table.items()))
        return '\n'.join(list(hash_table.values()))
    elif request.method == 'POST':
        # Обробка POST запиту
        data = request.get_json()
        key = list(data.keys())[0]
        hash_table[key] = data[key]
        print("Hash Table:", hash_table)
        return f"Message: {data[key]}"
    else:
        return jsonify({'error': 'Непідтримуваний метод запиту'})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
