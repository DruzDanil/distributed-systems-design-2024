from flask import Flask, jsonify, request
from hazelcast.client import HazelcastClient
import sys
from subprocess import Popen, CREATE_NEW_CONSOLE
from psutil import Process
from time import sleep
import consul
import json
c = consul.Consul()
cmd_proc = Popen(**json.loads(c.kv.get('hz-node')[1]['Value']))
sleep(2)
parent = Process(cmd_proc.pid)
child_proc = parent.children(recursive = True)
hz_proc = child_proc[2]

print(c.kv.get('map')[1]['Value'])
client = HazelcastClient(**json.loads(c.kv.get('hz')[1]['Value']))
lab3_map = client.get_map(c.kv.get('map')[1]['Value'].decode()).blocking()

app = Flask(__name__)

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        print("Hash msg:", lab3_map.values())
        ret = dict(lab3_map.entry_set())
        return ret
    elif request.method == 'POST':
        # Обробка POST запиту
        data = request.get_json()
        key = list(data.keys())[0]
        msg = data[key]
        lab3_map.put(key, msg)
        print("Receive message:", msg)
        return f"Message: {msg}"
    else:
        return jsonify({'error': 'Непідтримуваний метод запиту'})


if __name__ == '__main__':
    try:
        arg = sys.argv[1:][0]
        print("Arg:", arg)
    except:
        arg = None
    c.agent.service.register(
    name='logging-service',
    service_id=f'logging-service:{arg}',
    address="127.0.0.1",
    port=int(arg)
    )
    app.run(port=arg)
    client.shutdown()
    hz_proc.terminate()
