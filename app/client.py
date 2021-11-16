
from ctypes import resize
from datetime import datetime
from threading import Thread
import zmq
import asyncio
import json
from kademlia.network import Server
from zmq.sugar.constants import NULL
from types import SimpleNamespace
from collections import namedtuple
from queue import Queue

import Employee
import User
import Job_type as jt
import Academic_formation as af
import re
import datetime 
import time

# The subscriber thread requests messages starting with
# A and B, then reads and counts incoming messages.

def subscriber_thread(user):
    ctx = zmq.Context.instance()
    # Subscribe to "A" and "B"
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:6001")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")
    #subscriber.setsockopt(zmq.SUBSCRIBE, opc2.encode('utf-8'))

    while True:
        try:
            msg = subscriber.recv_multipart()
            #print(msg)
            if(len(msg[0].decode())>5):
                data = msg[0].decode()
                data = data.split(" ")
                resul = data[2].split(",")
                if(resul[0] == user):
                    print("Trabajo encontrado: ")
                    resul = data[2].split(",")
                    print("Nombre del trabajo: "+resul[4])
                    print("Tipo de trabajo: "+resul[1])
                    print("Hora de la reunion: "+resul[2])
                    print("Empleador a cargo: "+resul[3])
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted
            else:
                raise

def validate_user(user):
    resul = str(user).split(" ")
    date = str(datetime.datetime.now())
    resul[9] = date
    resul.pop(10)
    context = zmq.Context()
    #  Socket to talk to server
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://25.12.72.51:5555")
    resul = ' '.join(resul)
    print(resul)
    socket.send(str(resul).encode())
    #socket.send(str(123).encode())
    return socket.recv().decode()

def createUser(emplo):
    context = zmq.Context()
    #  Socket to talk to server
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://25.12.72.51:5555")
    socket.send(str(emplo).encode())
    return socket.recv().decode()


if __name__ == "__main__":
    
    cent = True
    data = ""
    while(cent):
        opc = input("1. Crear cuenta\n2. Iniciar sesion\n")

        emplo = NULL
    
        if(opc == str(1)):
            username = input ("Ingrese su usuario: ")
            password = input ("Ingrese su contrasena: ")
            emplo = Employee.Employee(username, password, "create")
            emplo.age = input ("Ingrese su edad: ")
            emplo.JO_categories.append(jt.Job_type(int(input("Ingrese la primera categoria de trabajo a escoger:\nFUERZAS_MILITARES = 1\nDIRECTORES_GERENTES = 2\nPROFESIONALES_CIENTIFICOS = 3\nTECNICOS_PROFESIONALES = 4\nPERSONAL_APOYO_ADM = 5\nTRABAJADORES_VENDEDORES = 6\n"))).name)
            emplo.JO_categories.append(jt.Job_type(int(input("Ingrese la segunda categoria de trabajo a escoger:\nFUERZAS_MILITARES = 1\nDIRECTORES_GERENTES = 2\nPROFESIONALES_CIENTIFICOS = 3\nTECNICOS_PROFESIONALES = 4\nPERSONAL_APOYO_ADM = 5\nTRABAJADORES_VENDEDORES = 6\n"))).name)
            emplo.capacities =input("Ingrese la capacidad: ")
            emplo.formation = af.Academic_formation(int(input("Ingrese su formación academica:\nPROFESIONAL = 1\nPOSGRADO = 2\nMAESTRIA = 3\nDOCTORADO = 4\n"))).name
                
            message = createUser(emplo)
            print("Cuenta creada con exito!! ahora inicia secion")
            cent = True

        if(opc == str(2)):
            while cent:
                username = input ("Ingrese su usuario: ")
                password = input ("Ingrese su contrasena: ")
                user = Employee.Employee(username, password, "validate")
                data = validate_user(user)
                if(data != "False"):
                    cent = False

    res = data.split(" ")
    cat1 = res[8][2:]
    cat1 = cat1[:-2]

    cat2 = res[9][1:-2]

    hability = res[6]
    user = res[2]
    
    print(cat1)
    print(cat2)
    print(hability)
    print("----")
    
    s_thread = Thread(target=subscriber_thread, args=(user,))
    s_thread.start()

    
    #asyncio.run(validate_user(username,password))
    #subscriber_thread(opc, opc2)