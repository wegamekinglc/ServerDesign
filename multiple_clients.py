# -*- coding: utf-8 -*-

import zmq
from threading import Thread


def client(client_id, host, port):

    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    sock.connect("tcp://{0}:{1}".format(host, port+client_id))

    for i in range(30):
        sock.send_string('Hi there! this is client {0}'.format(client_id))
        message = sock.recv()
        print(message)


def start_threads(interface, port, workers=4):
    for i in range(workers):
        args = (i, interface, port)
        t = Thread(target=client, args=args)
        t.start()


if __name__ == "__main__":

    start_threads('10.63.6.149', 8890)
