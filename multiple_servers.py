# -*- coding: utf-8 -*-

from threading import Thread
import zmq


def server(server_id, interface, port):

    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.bind("tcp://{0}:{1}".format(interface, port+server_id))

    while True:
        message = sock.recv()
        print(message)
        sock.send_string("Server {0} is responding".format(server_id))


def start_threads(interface, port, workers=4):
    for i in range(workers):
        args = (i, interface, port)
        t = Thread(target=server, args=args)
        t.start()


if __name__ == "__main__":

    start_threads('10.63.6.149', 8890)
