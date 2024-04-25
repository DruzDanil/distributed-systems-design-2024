from hazelcast.client import HazelcastClient
import random

# import hazelcast.config
# Создаем конфигурацию клиента Hazelcast и добавляем адреса всех узлов кластера
config = {
    "cluster_name": "dev",
    "cluster_members": ["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"]
}
# config = hazelcast.config.Config()
# config.cluster_name = "my-cluster"
# config._cluster_members = ["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"]
# config.connection_timeout = 5
# Создаем экземпляр клиента Hazelcast
client = HazelcastClient(cluster_name = "dev", cluster_members = ["172.17.0.2:5701"], use_public_ip=True)
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

    rmap = client.get_replicated_map("replicated_map")
    for i in range(1, 1001):
        rmap.put(i, map.get(i))

# Task 4
def task4():
    topic = client.get_topic("my_topic").blocking()
    # Отправляем сообщение в тему

    for i in range(1, 101):
        topic.publish(i)

# Task 5
def task5():
    queue = client.get_queue("my_queue").blocking()

    for i in range(1, 101):
        queue.offer(i)

task3()
# task4()
# task5()
# Когда закончите работу с кластером, не забудьте закрыть клиента
client.shutdown()


