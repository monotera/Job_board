
import zmq
from random import randint
import time

LRU_READY = "\x01"

context = zmq.Context(1)

frontend = context.socket(zmq.ROUTER) # ROUTER
backend = context.socket(zmq.ROUTER) # ROUTER
frontend.bind("tcp://*:5555") # For clients
backend.bind("tcp://*:5556")  # For workers

poll_workers = zmq.Poller()
poll_workers.register(backend, zmq.POLLIN)

poll_both = zmq.Poller()
poll_both.register(frontend, zmq.POLLIN)
poll_both.register(backend, zmq.POLLIN)

identity = "%04X-%04X" % (randint(0, 0x10000), randint(0,0x10000))

print("I: (%s) loadbalancer ready" % identity)

workers = []

while True:
    if workers:
        socks = dict(poll_both.poll())
    else:
        socks = dict(poll_workers.poll())

    # Handle worker activity on backend
    if socks.get(backend) == zmq.POLLIN:
        print("Loadbalancer: server() Cuenta iniciada...")
        start_time = time.time()
        # Use worker address for LRU routing
        msg = backend.recv_multipart()
        
        if not msg:
            break
        address = msg[0]
        workers.append(address)

        # Everything after the second (delimiter) frame is reply
        reply = msg[2:]

        # Forward message to client if it's not a READY
        if reply[0] != LRU_READY:
            frontend.send_multipart(reply)
            elapsed_time = time.time() - start_time
            print("Loadbalancer: server() Tiempo transcurrido: ", str(elapsed_time))

    if socks.get(frontend) == zmq.POLLIN:
        print("Loadbalancer: client() Cuenta iniciada...")
        start_time = time.time()
        #  Get client request, route to first available worker
        msg = frontend.recv_multipart()
        request = [workers.pop(0), ''.encode()] + msg
        backend.send_multipart(request)
        elapsed_time = time.time() - start_time
        print("Loadbalancer: client() Tiempo transcurrido: ", str(elapsed_time))