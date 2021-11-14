
import zmq


# The subscriber thread requests messages starting with
# A and B, then reads and counts incoming messages.

def subscriber_thread(opc, opc2):
    ctx = zmq.Context.instance()

    opc = input("esperando filtro")

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

if __name__ == "__main__":
    opc = input ("Ingrese el primer trabajo: ")
    opc2 = input ("Ingrese el segundo trabajo: ")
    subscriber_thread(opc, opc2)