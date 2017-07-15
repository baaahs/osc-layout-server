
import cherrypy
from server import OSCLayoutServer
import argparse

argument_parser = argparse.ArgumentParser(description='BAAAHS OSC Layout Server')

argument_parser.add_argument('--layouts-dir', dest='layouts_directory', required=True, default='layouts', help='The directory containing OSC layouts')
argument_parser.add_argument('--cache-ttl', dest='cache_ttl', default=60, type=int, help='The cache TTL in seconds')
argument_parser.add_argument('--cache-max-entries', dest='cache_max_entries', default=20, type=int, help='The max number of entires allow in the cache')

arguments = argument_parser.parse_args()

port = 9658

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': port,
        'server.thread_pool': 5
    }
}

cherrypy.quickstart(OSCLayoutServer(arguments.layouts_directory, arguments.cache_ttl, arguments.cache_max_entries), config=config)
