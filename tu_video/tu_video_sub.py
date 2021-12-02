import time
import numpy
import zmq


def recv_array_and_str(socket, flags=0, copy=True, track=False):
    string = socket.recv_string(flags=flags)
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)

    img = numpy.frombuffer(bytes(memoryview(msg)), dtype=md["dtype"])
    return string, img.reshape(md["shape"])


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect("tcp://localhost:5667")

while True:
    time.sleep(1)
    print(recv_array_and_str(socket))
