import zmq


def main():
    """ main method """
    # Prepare our context and publisher
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5563")

    code_filter = "trabajador"

    subscriber.setsockopt_string(zmq.SUBSCRIBE, code_filter)

    while True:
        string = subscriber.recv_string()
        code_test, data = string.split()
        print(subscriber.identity)
        print(code_test)
        print(data)

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


if __name__ == "__main__":
    main()