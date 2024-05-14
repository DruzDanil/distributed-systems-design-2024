from flask import Flask, request, jsonify
import uuid
import requests
from random import choice
from hazelcast.client import HazelcastClient
import consul
import sys
import json

c = consul.Consul()
app = Flask(__name__)
logging_service_port = json.loads(c.kv.get('log_ports')[1]['Value'])
message_service_port = json.loads(c.kv.get('msg_ports')[1]['Value'])
client = HazelcastClient(**json.loads(c.kv.get('hz')[1]['Value']))
queue = client.get_queue(c.kv.get('queue')[1]['Value'].decode()).blocking()
def get_url(service_name):
    open_addrs = []
    services = c.health.service(service_name)[1]
    for service in services:
        addrs = service['Service']['Address']
        port = service['Service']['Port']
        open_addrs.append(f'{addrs}:{port}')
    return open_addrs


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        # Обробка GET запиту
        open_logs_addrs = get_url('logging-service')
        open_msgs_addrs = get_url('message-service')
        log_addrs = choice(open_logs_addrs)
        mess_addrs = choice(open_msgs_addrs)
        response1 = requests.get(f'http://{log_addrs}/data').json()
        response2 = requests.get(f'http://{mess_addrs}/data').json()
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
        open_logs_addrs = get_url('logging-service')
        log_addrs = choice(open_logs_addrs)
        response = requests.post(f'http://{log_addrs}/data', json=data)
        print("Response", response.text)
        data = response.text
        return data
    else:
        return 'Непідтримуваний метод запиту'

if __name__ == '__main__':
    try:
        arg = int(sys.argv[1:][0])
        print("Arg:", arg)
    except:
        arg = None
    c.agent.service.register(
    name='facade-service',
    service_id=f'facade-service:{arg}',
    address="127.0.0.1",
    port=arg
    )
    app.run(port=arg)
    client.shutdown()
