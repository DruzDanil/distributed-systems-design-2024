from hazelcast.client import HazelcastClient
import random

client = HazelcastClient(cluster_name="dev")
# Печатаем информацию о кластере
cluster = client.cluster_service
print("Cluster Members:")
for member in cluster.get_members():
    print(member.address)
# Выполняем действия в кластере...
# Task 3
def task3():
    map = client.get_map("map").blocking()
    for i in range(1, 1001):
        map.put(i, random.randint(1, 1000))

# Task 4
def task4():
    topic = client.get_topic("my_topic").blocking()

    for i in range(1, 101):
        topic.publish(i)

# Task 5
def task5():
    queue = client.get_queue("default").blocking()

    for i in range(1, 101):
        queue.offer(i, 10)
        

task3()
task4()
task5()

client.shutdown()


