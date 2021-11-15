
import time

from random import randint
from string import ascii_uppercase as uppercase
from threading import Thread

import zmq
from zmq.devices import monitored_queue

from ..Resources import zhelpers as zh


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

def main ():

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

if __name__ == '__main__':
    main()