#!/usr/bin/env python2.7
import cherrypy
from server import OSCLayoutServer
import argparse

argument_parser = argparse.ArgumentParser(description='BAAAHS OSC Layout Server')

argument_parser.add_argument('--layout', dest='layout_file', required=True, help='The layout to serve')

arguments = argument_parser.parse_args()

port = 9658

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': port,
        'server.thread_pool': 1
    }
}

cherrypy.quickstart(OSCLayoutServer(arguments.layout_file), config=config)
