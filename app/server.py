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
from random import randrange

numUser = 0

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
                res[-1] = data_split[-1]
                res[-2] = data_split[-2]
                cent = " ".join(res)
                await server.set(data_split[2],cent)

        elif cent == "offer":
            cent = ""
            print(data_split)
            require_job = data_split[5]
            require_hab = data_split[6]
            date_job = data_split[-2]
            owner_job = data_split[-1]
            raw_values = server.storage.data.values()
            list_values = list(raw_values)
            candidates = []
            for value in list_values:
                value_split = value[1].split(" ") 
                cat1 = value_split[8][2:-2]
                cat2 = value_split[9][1:-2]
                
                if value_split[1] == "0" and value_split[5] == "True" and int(data_split[3]) > 0:
                    if value_split[6] == require_hab and (require_job == cat1 or require_job == cat2):
                        candidates.append(value_split[2] + ","+ require_job + "," + date_job+ "," + owner_job)
                        #cent = cent + " | " + value_split[2] + ","+ require_job + "," + date_job +" | "
                number_vacancy = int(data_split[3])

                counter = 0
            for i in range(len(candidates)):
                cent = cent + " | "+ candidates[i]
                counter += 1
                if(counter > number_vacancy):
                    break
            
            data_split[3] = str(number_vacancy - counter)

            key = data_split[-1] + "-" + data_split[2]
            offer_data = " ".join(data_split)

            await server.set(key, offer_data)

            json_data = dict(aps=data_split)
            with open('resultado.json') as f:
                anteriores = json.load(f)

            anteriores[f'{key}'] = json_data['aps']

            with open('resultado.json', 'w') as file:
                json.dump(anteriores, file, indent=4, default=str)

                    

            
            

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

