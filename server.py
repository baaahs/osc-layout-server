import cherrypy
import os
import zipfile
from cachetools import TTLCache

class OSCLayoutServer(object):

    osc_zipfile = 'index.xml'
    layouts_directory = 'layouts'
    ttl_cache_timeout_in_seconds = 60
    cache_max_entries = 20
    cache = TTLCache(maxsize=cache_max_entries, ttl=ttl_cache_timeout_in_seconds)

    def __init__(self):
        _layouts_path = os.path.join(os.path.dirname(__file__), self.layouts_directory)
        self.layouts = set(os.listdir(_layouts_path))

    @cherrypy.expose
    def index(self):

        client_ip = cherrypy.request.remote.ip

        if self.cache.__contains__(client_ip):

            transmitted_layouts = self.cache[client_ip]
            pending_transmission_layouts = self.layouts.difference(transmitted_layouts)

            if pending_transmission_layouts:

                layout_to_transmit = pending_transmission_layouts.pop()
                transmitted_layouts.add(layout_to_transmit)

            else:

                raise cherrypy.HTTPError(404, "Client has received all layouts")

        else:

            layout_to_transmit = self.layouts.copy().pop()

            self.cache[client_ip] = {layout_to_transmit}

        cherrypy.response.headers['Content-type'] = 'application/touchosc'
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="' + layout_to_transmit + '"'

        osc_layout_file_full_path = os.path.join(os.path.dirname(__file__), self.layouts_directory, layout_to_transmit)
        osc_layout_zipfile = zipfile.ZipFile(osc_layout_file_full_path)

        return osc_layout_zipfile.open(self.osc_zipfile, 'r')
