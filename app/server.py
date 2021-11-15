import time
import zmq
import json
import asyncio
from types import SimpleNamespace
from random import randint

from kademlia.network import Server
from zmq.sugar.constants import NULL
import Employee
from collections import namedtuple

numUser = 0

async def validate_user(msg):
    data = msg.split(" ")
    server = Server()
    await server.listen(8469)
    bootstrap_node = ("127.0.0.2", 8469)
    await server.bootstrap([bootstrap_node])

    result = await server.get("Carlos")
    print(result)
    data2 = result.split(" ")
    server.stop()

    if data2[3] == data[3]:
        return result
    return NULL

        
async def add_user(msg):
    data = msg.split(" ")
    server = Server()
    await server.listen(8469)
    bootstrap_node = ("127.0.0.1", 8469)
    await server.bootstrap([bootstrap_node])
    await server.set("Carlos", "msg")
    server.stop()
    return True;

def process_str(msg):
    data = msg.split(" ")
    return data[0]


async def main():
    server = Server()
    await server.listen(8469)
    bootstrap_node = ("127.0.0.2", 8469)
    await server.bootstrap([bootstrap_node])

    with open('resultado.json') as f:
        anteriores = json.load(f)

    print("Cargando datos ...")

    for user in anteriores:
        str1 = ' '.join(anteriores[f'{user}'])
        print(str1)
        await server.set(user, str1)

    print("... Datos cargados")


    
    
    while True:
        
        msg = worker.recv_multipart()
        if not msg:
            break

        cent = process_str(msg[2].decode())
        data = msg[2].decode()
        data_split = data.split(" ")
        if(cent == "create"):
            await server.set(data_split[2], data)

            json_data = dict(aps=data_split)
            with open('resultado.json') as f:
                anteriores = json.load(f)

            anteriores[f'{data_split[2]}'] = json_data['aps']
            
            with open('resultado.json', 'w') as file:
                json.dump(anteriores, file, indent=4, default=str)

            cent = False
        elif(cent == "validate"):
            cent = await server.get(data_split[2])
            res = cent.split(" ")
            if(res[3] != data_split[3]):
                cent = False
        else:
            print("Process: ")
            
        
        msg[2] = str(cent).encode()
        print("I: (%s) normal reply" % identity)
        
        worker.send_multipart(msg)


LRU_READY = "\x01"

context = zmq.Context(1)
worker = context.socket(zmq.REQ)

identity = "%04X-%04X" % (randint(0, 0x10000), randint(0,0x10000))
worker.setsockopt_string(zmq.IDENTITY, identity)
worker.connect("tcp://localhost:5556")

print("I: (%s) server ready" % identity)
worker.send_string(LRU_READY)

asyncio.run(main())




        
"""

while True:

    
    #  Wait for next request from client
    message = socketFiltro.recv_pyobj()
    print(f"Received request: {message}")

    if(message.funct == "validate"):
        print(message.username)
        asyncio.run(validate_user(message.username, message.password))
    elif(message.funct == "create"):
        
        asyncio.run(add_user(message.name, str(message)))

        with open('resultado.json', 'w') as file:
            json.dump(str(message), file, indent=4)

        #  Send reply back to client
        socketFiltro.send_string("OK")
"""