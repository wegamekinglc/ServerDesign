# -*- coding: utf-8 -*-

import zmq
from threading import Thread


def client(client_id, host, port):

    context = zmq.Context()
    sock = context.socket(zmq.REQ)

    # connect to controller to ask for server destination
    sock.connect("tcp://{0}:{1}".format(host, port))
    sock.send_string("Hi controller! this is client {0}".format(client_id))
    message = sock.recv_json()
    sock.close()

    # connect to actual working server
    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    server_interface = message['interface']
    server_port = message['port']
    sock.connect("tcp://{0}:{1}".format(server_interface, server_port))

    for i in range(15):
        sock.send_string('Hi server! this is client {0} for the {1}th time'.format(client_id, i))
        message = sock.recv()
        print(message + ' to client {0}'.format(client_id))

    sock.close()


def simulated_multiple_clients(interface, port, clients=15):
    for i in range(clients):
        args = (i, interface, port)
        t = Thread(target=client, args=args)
        t.start()


if __name__ == "__main__":

    simulated_multiple_clients(interface='127.0.0.1',
                               port=8890,
                               clients=15)
