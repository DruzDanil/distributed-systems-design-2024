from flask import Flask
from hazelcast.client import HazelcastClient
import sys
import threading
import signal
app = Flask(__name__)
facade_server_url = 'http://127.0.0.1:5000'
client = HazelcastClient(cluster_name="dev")
queue = client.get_queue("queue").blocking()
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
    arg = sys.argv[1:][0]
    event_thread = threading.Thread(target= queue_event)
    event_thread.start()
    app.run(port=arg)


