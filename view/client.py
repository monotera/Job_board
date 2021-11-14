
from ctypes import resize
import zmq
import asyncio
from kademlia.network import Server

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

async def validate_user(username, password):
        server = Server()
        await server.listen(8469)
        bootstrap_node = ("127.0.0.1", 8469)
        await server.bootstrap([bootstrap_node])

        await server.set("usuario","pass")
        result = await server.get(username)
        server.stop()
        if result == password:
            return True
        return False

if __name__ == "__main__":
    
    username = input ("Ingrese su usuario: ")
    password = input ("Ingrese su contrasena: ")
    

    while not asyncio.run(validate_user(username,password)):
        username = input ("Ingrese su usuario: ")
        password = input ("Ingrese su contrasena: ")

    opc = input ("Ingrese el primer trabajo: ")
    opc2 = input ("Ingrese el segundo trabajo: ")
    subscriber_thread(opc, opc2)