
import cherrypy
import os
import zipfile

class OSCLayoutServer(object):

    osc_zipfile = 'index.xml'
    layouts_directory = 'layouts'

    def __init__(self):
        _layouts_path = os.path.join(os.path.dirname(__file__), self.layouts_directory)
        self._layouts = os.listdir(_layouts_path)

        # select first layout as default
        self._selectedLayout = self._layouts[0]

    @cherrypy.expose()
    @cherrypy.tools.json_out()
    def current_layout(self):

        return {'layout': self._selectedLayout}

    @cherrypy.expose()
    def set_layout(self, layout):

        if layout in self._layouts:
            self._selectedLayout = layout
        else:
            raise cherrypy.HTTPError(404, "The server is unaware of the supplied layout: " + layout)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def layouts(self):

        return {'layouts': self._layouts}

    @cherrypy.expose
    def index(self):

        cherrypy.response.headers['Content-type'] = 'application/touchosc'
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="' + self._selectedLayout + '"'

        _osc_layout_file_fullpath = os.path.join(os.path.dirname(__file__), self.layouts_directory, self._selectedLayout)
        _osc_layout_zipfile = zipfile.ZipFile(_osc_layout_file_fullpath)

        return _osc_layout_zipfile.open(self.osc_zipfile, 'r')
