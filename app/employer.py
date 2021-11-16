
from random import randint
from string import ascii_uppercase as uppercase
from threading import Thread

import zmq
import time

from zmq.sugar.constants import NULL
import Employee
import Job_offer
import datetime

# publisher thread
# The publisher sends random messages starting with A-J:

def publisher_thread():
    ctx = zmq.Context.instance()

    publisher = ctx.socket(zmq.PUB)
    publisher.bind("tcp://*:6000")

    while True:
        opc = input("Desea ingresar una oferta de trabajo (S/N): ")
        offer = Job_offer.JobOffer()
        print(str(offer))

        try:
            publisher.send(str(offer).encode())
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted
            else:
                raise
        time.sleep(0.1)         # Wait for 1/10th second

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
            emplo = Employee.Employee(username, password, "createEmployer")
            message = createUser(emplo)
            print("Cuenta creada con exito!! ahora inicia secion")
            cent = True

        if(opc == str(2)):
            while cent:
                username = input ("Ingrese su usuario: ")
                password = input ("Ingrese su contrasena: ")
                user = Employee.Employee(username, password, "validateEmployer")
                data = validate_user(user)
                if(data != "False"):
                    cent = False
    


    p_thread = Thread(target=publisher_thread, args=())
    p_thread.start()