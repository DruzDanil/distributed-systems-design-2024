from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
facade_server_url = 'http://127.0.0.1:5000'

@app.route('/data', methods=['GET'])
def data():
    # Обробка GET запиту
    return "not implemented yet"

if __name__ == '__main__':
    app.run(port=5001)


