# -*- coding: utf-8 -*-

import zmq
import time


def server(server_id, interface, port, container):

    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.bind("tcp://{0}:{1}".format(interface, port))
    print('Server {0} is listening'.format(server_id))

    while True:
        message = sock.recv()
        print(message + ' to Server {0}'.format(server_id))
        sock.send_string("Server {0} is responding".format(server_id))
        container.put({'server': server_id, 'message': message})
        time.sleep(5)

