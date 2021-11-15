
from ctypes import resize
import zmq
import asyncio
import json
from kademlia.network import Server
from zmq.sugar.constants import NULL
from types import SimpleNamespace
from collections import namedtuple

import Employee
import User
import Job_type as jt

# The subscriber thread requests messages starting with
# A and B, then reads and counts incoming messages.

def subscriber_thread(opc, opc2):
    ctx = zmq.Context.instance()


    # Subscribe to "A" and "B"
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:6001")
    subscriber.setsockopt(zmq.SUBSCRIBE, opc.encode('utf-8'))
    subscriber.setsockopt(zmq.SUBSCRIBE, opc2.encode('utf-8'))

    count = 0
    while count < 5:
        try:
            msg = subscriber.recv_multipart()
            print(msg)
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted
            else:
                raise
        count += 1

    print ("Subscriber received %d messages" % count)

def validate_user(user):
    context = zmq.Context()
    #  Socket to talk to server
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send(str(user).encode())
    #socket.send(str(123).encode())
    return socket.recv().decode()
    



def createUser(emplo):
    context = zmq.Context()
    #  Socket to talk to server
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send(str(emplo).encode())
    return socket.recv().decode()


if __name__ == "__main__":

    cent = True

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
            cent2 = True
            while(cent2):
                opc2 = input("Desea agregar una nueva capacidad (S/N): ")
                if(opc2 == "S"):
                    emplo.capacities.addCapacity(input("Ingrese la capacidad: "))
                else:
                    cent2 = False
            message = createUser(emplo)
            print(message)
            if(message != NULL):
                cent = False

        if(opc == str(2)):
            while cent:
                username = input ("Ingrese su usuario: ")
                password = input ("Ingrese su contrasena: ")
                user = Employee.Employee(username, password, "validate")
                data = validate_user(user)
                print(data)
                if(data != NULL):
                    cent = False
            

    
    #asyncio.run(validate_user(username,password))
    #subscriber_thread(opc, opc2)