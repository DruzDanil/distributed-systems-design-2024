from flask import Flask, jsonify, request
from hazelcast.client import HazelcastClient
import sys
from subprocess import Popen, CREATE_NEW_CONSOLE
from psutil import Process
from time import sleep

cmd_proc = Popen("C:\\Users\\Люциус\\Desktop\\DSD\\hazelcast-5.4.0\\bin\\hz-start.bat", creationflags = CREATE_NEW_CONSOLE)
sleep(2)
parent = Process(cmd_proc.pid)
child_proc = parent.children(recursive = True)
hz_proc = child_proc[2]


client = HazelcastClient(cluster_name="dev")
lab3_map = client.get_map("lab3_map").blocking()

app = Flask(__name__)
facade_server_url = 'http://127.0.0.1:5000'

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
    arg = sys.argv[1:][0]
    app.run(port=arg)
    client.shutdown()
    hz_proc.terminate()
