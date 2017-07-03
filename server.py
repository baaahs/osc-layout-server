
import cherrypy
import os
import zipfile
import itertools

class OSCLayoutServer(object):

    osc_zipfile = 'index.xml'
    layouts_directory = 'layouts'

    def __init__(self):
        _layouts_path = os.path.join(os.path.dirname(__file__), self.layouts_directory)
        self._layouts = itertools.cycle(os.listdir(_layouts_path))

    @cherrypy.expose
    def index(self):

        _layout = self._layouts.next()

        cherrypy.response.headers['Content-type'] = 'application/touchosc'
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="' + _layout + '"'

        _osc_layout_file_fullpath = os.path.join(os.path.dirname(__file__), self.layouts_directory, _layout)
        _osc_layout_zipfile = zipfile.ZipFile(_osc_layout_file_fullpath)

        return _osc_layout_zipfile.open(self.osc_zipfile, 'r')
