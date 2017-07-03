
import cherrypy
from server import OSCLayoutServer

port = 9658

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': port
    }
}

cherrypy.quickstart(OSCLayoutServer(), config=config)
