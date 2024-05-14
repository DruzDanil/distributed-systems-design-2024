from flask import Flask, request, jsonify
import uuid
import requests
from random import choice
from hazelcast.client import HazelcastClient

app = Flask(__name__)
url = 'http://127.0.0.1'
logging_service_port = [5002, 5003, 5004]
message_service_port = [5005, 5006]
client = HazelcastClient(cluster_name="dev")
queue = client.get_queue("queue").blocking()

import socket

def open_ports(ports):
    opened_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', port))
            if result == 0:
                opened_ports.append(port)      
        except socket.error:
            if port in open_ports:
                opened_ports.remove(port)   
        finally:
            sock.close()
    return opened_ports

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        # Обробка GET запиту
        open_log_ports = open_ports(logging_service_port)
        open_msg_ports = open_ports(message_service_port)
        if len(open_log_ports) == 0:
            return "Logging service недоступний"
        if len(open_msg_ports) == 0:
            return "Message service недоступний"
        log_port = choice(open_log_ports)
        mess_port = choice(open_msg_ports)
        response1 = requests.get(f'{url}:{log_port}/data').json()
        response2 = requests.get(f'{url}:{mess_port}/data').json()
        return jsonify({'message-service': response2, 'logging-service': response1})
    elif request.method == 'POST':
        # Обробка POST запиту
        msg = request.get_data().decode('utf-8')
        print("value:", msg)
        unique_id = uuid.uuid4()
        print("UID:", unique_id)
        data = {f'{unique_id}': msg}
        print("Data:", data)
        queue.offer(msg)
        open_log_ports = open_ports(logging_service_port)
        if len(open_log_ports) == 0:
            return "Сервіс недоступний"
        log_port = choice(open_log_ports)
        response = requests.post(f'{url}:{log_port}/data', json=data)
        print("Response", response.text)
        data = response.text
        return data
    else:
        return 'Непідтримуваний метод запиту'

if __name__ == '__main__':
    app.run()
    client.shutdown()
