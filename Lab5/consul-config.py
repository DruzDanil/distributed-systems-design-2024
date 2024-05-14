import consul
from subprocess import Popen, CREATE_NEW_CONSOLE
# from psutil import Process
import json
# from time import sleep
# cmd_proc = Popen(["C:\\Users\\Люциус\Desktop\\DSD\\consul.exe", "agent", "-dev"], creationflags = CREATE_NEW_CONSOLE)
# sleep(2)
# parent = Process(cmd_proc.pid)
# child_proc = parent.children(recursive = True)
# hz_proc = child_proc[2]

c = consul.Consul()
c.kv.put('log_ports', json.dumps([5002, 5003, 5004]))
c.kv.put('msg_ports', json.dumps([5005, 5006]))
configs = {
    'cluster_name': 'dev'
}
c.kv.put('hz', json.dumps(configs))
c.kv.put('queue', 'queue')
configs = {
    'args': "C:\\Users\\Люциус\\Desktop\\DSD\\hazelcast-5.4.0\\bin\\hz-start.bat",
    'creationflags': CREATE_NEW_CONSOLE
}
c.kv.put('hz-node', json.dumps(configs))
c.kv.put('map', 'my-map')