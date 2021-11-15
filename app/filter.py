
from socket import socket
import time

from random import randint
from string import ascii_uppercase as uppercase
from threading import Thread
from queue import Queue

import zmq
from zmq.devices import monitored_queue

import zhelpers as zh


# listener thread
# The listener receives all messages flowing through the proxy, on its
# pipe. Here, the pipe is a pair of ZMQ_PAIR sockets that connects
# attached child threads via inproc. In other languages your mileage may vary:


def listener_thread (pipe):
    
    # Print everything that arrives on pipe
    cont = 0
    while True:
        if(cont == 3):
            print("Hola")
        cont += 1
        try:
            print (pipe.recv_multipart(), "p")
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted


# main thread
# The main task starts the subscriber and publisher, and then sets
# itself up as a listening proxy. The listener runs as a child thread:

def subscriber_thread(request_q):

    ctx = zmq.Context.instance()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:6000")
    subscriber.setsockopt(zmq.SUBSCRIBE, b'');

    while(True):
        try:
            msg = subscriber.recv_multipart()
            request_q.put(msg)
            print(msg)
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted
            else:
                raise

def publisher_thread(reply_q):

    ctx = zmq.Context.instance()
    publisher = ctx.socket(zmq.PUB)
    publisher.bind("tcp://*:6001")
    while(True):
        msg = reply_q.get()
        try:
            publisher.send(msg.encode())
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                break           # Interrupted
            else:
                raise
        time.sleep(0.1)         # Wait for 1/10th second

def server_thread(request_q, reply_q):
    while(True):
        if(request_q.qsize()>10):
            for i in range(10):
                context = zmq.Context()
                socket = context.socket(zmq.REQ)
                socket.connect("tcp://localhost:5555")
                msg = request_q.get()
                print(msg)
                socket.send_multipart(msg)
                reply_q.put(socket.recv().decode())

def main ():

    request_q = Queue()
    reply_q = Queue()

    s_thread = Thread(target=subscriber_thread, args=(request_q,))
    s_thread.start()

    p_thread = Thread(target=publisher_thread, args=(reply_q,))
    p_thread.start()

    ser_thread = Thread(target=server_thread, args=(request_q, reply_q, ))
    ser_thread.start()

    

    """
    # Start child threads
    ctx = zmq.Context.instance()
    #p_thread = Thread(target=publisher_thread)
    #s_thread = Thread(target=subscriber_thread)
    #p_thread.start()
    #s_thread.start()

    pipe = zh.zpipe(ctx)

    subscriber = ctx.socket(zmq.XSUB)
    subscriber.connect("tcp://localhost:6000")

    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://*:6001")

    l_thread = Thread(target=listener_thread, args=(pipe[1],))
    l_thread.start()

    try:
        monitored_queue(subscriber, publisher, pipe[0], b'pub', b'sub')

    except KeyboardInterrupt:
        print ("Interrupted")

    del subscriber, publisher, pipe
    ctx.term()
    """

if __name__ == '__main__':
    main()