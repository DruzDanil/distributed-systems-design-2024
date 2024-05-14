from flask import Flask
from hazelcast.client import HazelcastClient
import sys
import threading
import consul
import json
import signal

c = consul.Consul()
app = Flask(__name__)
client = HazelcastClient(**json.loads(c.kv.get('hz')[1]['Value']))
queue = client.get_queue(c.kv.get('queue')[1]['Value'].decode()).blocking()
message_list = []

running = True

def signal_handler(sig, frame):
    global running
    running = False
    client.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
def queue_event():
    i = 1
    while running:
            try:
                poll = queue.take()
            except Exception:
                continue
            message_list.append(poll)
            print(f"{i}. Get message: {poll}")
            i += 1

@app.route('/data', methods=['GET'])
def data():
    # Обробка GET запиту
    print("Messages list:", message_list)
    return message_list

if __name__ == '__main__':
    try:
        arg = sys.argv[1:][0]
        print("Arg:", arg)
    except:
        arg = None
    c.agent.service.register(
    name='message-service',
    service_id=f'message-service:{arg}',
    address="127.0.0.1",
    port=int(arg)
    )
    event_thread = threading.Thread(target=queue_event)
    event_thread.start()
    app.run(port=arg)


