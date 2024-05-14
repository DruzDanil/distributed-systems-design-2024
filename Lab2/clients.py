from hazelcast.client import HazelcastClient

client = HazelcastClient(cluster_name='dev')

# Task 4
def on_message(message):
        print("Received message:", message)
def task4():
    print("Task4")
    topic = client.get_topic("my_topic").blocking()
    topic.add_listener(on_message)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

# Task 5
def read_from_queue():
    queue = client.get_queue("default").blocking()
    try:
        i = 1
        while True:
            poll = queue.poll()
            if poll != None:
                print(f"{i}. Item: {poll}")
                i += 1
    except KeyboardInterrupt:
        pass
def task5():
    read_from_queue()

task4()
task5()

client.shutdown()