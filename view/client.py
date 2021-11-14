import time
import zmq


def main():
    """main method"""

    # Prepare our context and publisher
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    # TODO: set ident
    publisher.identity = u"Client-{}".format(1).encode("ascii")
    publisher.bind("tcp://*:5563")

    name = input("Esperando filtro")

    code = "trabajador"
    data = "123"


    publisher.send_string(f"{code} {data}")
    code = "10002"
    data = "123asda"
    publisher.send_string(f"{code} {data}")
    code = "trabajador"
    data = "123123"
    publisher.send_string(f"{code} {data}")

    time.sleep(1)

    # We never get here but clean up anyhow
    publisher.close()
    context.term()


if __name__ == "__main__":
    main()