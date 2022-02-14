import simplejpeg
import zmq


# publish video stream to endpoints
def tu_video_pub(socket, image, data, flags=0):
    image = simplejpeg.encode_jpeg(image)
    socket.send_json(data, flags | zmq.SNDMORE)
    return socket.send(image, flags)


# subscribe video stream ing endpoints
def tu_video_sub(socket, flags=0, copy=True, track=False):
    data = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    img = simplejpeg.decode_jpeg(msg)
    return data, img


# create pub socket
def tu_video_create_pub(ip, port):
    pub_context = zmq.Context()
    pub_socket = pub_context.socket(zmq.PUB)
    pub_socket.bind("tcp://" + str(ip) + ":" + str(port))
    return pub_socket


# create sub socket
def tu_video_create_sub(ip, port):
    sub_context = zmq.Context()
    sub_socket = sub_context.socket(zmq.SUB)
    sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
    sub_socket.connect("tcp://" + str(ip) + ":" + str(port))
    return sub_socket
