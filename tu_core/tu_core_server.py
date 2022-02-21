import tu_settings

# get monkey from gevent
from gevent import monkey

# patch I/Os for async operations
monkey.patch_all()

# get server and applications
from gevent.pywsgi import WSGIServer
from tu_core_server_api import application

# api will run on port 80 with root privileges, else 8080 port
if __name__ == "__main__":

    # start the application on port 80, needs root privileges on linux
    server_frontend = WSGIServer(listener=(tu_settings.tu_core_server_ip, tu_settings.tu_core_server_port),
                                 application=application,
                                 log=application.logger)
    server_frontend.serve_forever()
