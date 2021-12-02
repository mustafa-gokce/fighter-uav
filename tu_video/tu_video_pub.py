import time
import numpy
import zmq


def send_array_and_str(socket, img, string, flags=0):
    md = dict(dtype=str(img.dtype), shape=img.shape)

    socket.send_string(string, flags | zmq.SNDMORE)
    socket.send_json(md, flags | zmq.SNDMORE)
    return socket.send(img, flags)


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5667")

my_ndarray = numpy.array([1, 2, 3])
my_string = "Hello World"

while True:
    time.sleep(1)
    send_array_and_str(socket, my_ndarray, my_string)
