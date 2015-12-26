# -*- coding: utf-8 -*-

from threading import Thread
import zmq
from server import server
try:
    from Queue import Queue
except ImportError:
    from queue import Queue


def controller(interface, port, container, workers):
    client_count = 0

    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.bind("tcp://{0}:{1}".format(interface, port))
    print('Controller is listening')

    # start all the working threads

    working_server = []

    for i in range(workers):
        args = (i, interface, port + i + 1, container)
        t = Thread(target=server, args=args)
        t.daemon = True
        t.start()
        working_server.append({'interface': interface,
                               'port': port + i + 1})

    # do the scheduling for incoming request
    while True:
        message = sock.recv()
        print(message.decode('ascii') + ' to Controller')
        cur = client_count % workers
        sock.send_json(working_server[cur])
        print(working_server[cur])
        client_count += 1

if __name__ == "__main__":

    # global container
    queue = Queue()

    controller(interface='127.0.0.1',
               port=8890,
               container=queue,
               workers=8)

    while queue.qsize():
        print(queue.get())
