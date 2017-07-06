import cherrypy
import os
import zipfile
from cachetools import TTLCache

class OSCLayoutServer(object):

    osc_zipfile = 'index.xml'
    layouts_directory = 'layouts'
    ttl_cache_timeout_in_seconds = 60
    cache_max_entries = 30
    cache = TTLCache(maxsize=cache_max_entries, ttl=ttl_cache_timeout_in_seconds)

    def __init__(self):
        _layouts_path = os.path.join(os.path.dirname(__file__), self.layouts_directory)
        self.layouts = os.listdir(_layouts_path)

    @cherrypy.expose
    def index(self):

        client_ip = cherrypy.request.remote.ip

        if self.cache.__contains__(client_ip):

            served_client_layouts = self.cache[client_ip]
            yet_to_be_served_client_layouts = list(set(self.layouts).difference(set(served_client_layouts)))

            if yet_to_be_served_client_layouts:

                layout_to_serve = yet_to_be_served_client_layouts[0]
                served_client_layouts.append(layout_to_serve)

            else:

                raise cherrypy.HTTPError(404, "Client has received all layouts")

        else:

            layout_to_serve = self.layouts[0]

            self.cache[client_ip] = [layout_to_serve]

        cherrypy.response.headers['Content-type'] = 'application/touchosc'
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="' + layout_to_serve + '"'

        osc_layout_file_fullpath = os.path.join(os.path.dirname(__file__), self.layouts_directory, layout_to_serve)
        osc_layout_zipfile = zipfile.ZipFile(osc_layout_file_fullpath)

        return osc_layout_zipfile.open(self.osc_zipfile, 'r')
