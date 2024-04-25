from hazelcast.client import HazelcastClient

config = {
    "cluster_name": "my-cluster",
    "network": {
        "cluster_members": ["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"],
        "connection_timeout": 5
    },
    "replicated_map_config": {
        "replicated_map_name": "my_replicated_map"
    }
}

client = HazelcastClient(**config)

client.start()
# Task 4
def on_message(message):
        print("Received message:", message)
def task4():
    topic = client.get_topic("my_topic").blocking()
    topic.add_listener(on_message)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

# Task 5
def read_from_queue():
    queue = client.get_queue("my_queue").blocking()
    try:
        while True:
            print("Item:", queue.poll())
    except KeyboardInterrupt:
        pass
def task5():
    read_from_queue()

client.shutdown()