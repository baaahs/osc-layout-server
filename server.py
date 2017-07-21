import cherrypy
import os
import zipfile

class OSCLayoutServer(object):

    osc_zipfile = 'index.xml'

    def __init__(self, layout_file):

        absolute_layout_path = os.path.join(os.path.dirname(__file__), layout_file)

        print absolute_layout_path

        if not os.path.isfile(absolute_layout_path):
            raise RuntimeError('There are no layouts in the layout directory selected')

        self.layout_file = layout_file
        self.absolute_layout_path = absolute_layout_path

    @cherrypy.expose
    def index(self):

        cherrypy.response.headers['Content-type'] = 'application/touchosc'
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename="' + self.layout_file + '"'

        osc_layout_file_full_path = os.path.join(os.path.dirname(__file__), self.layout_file)
        osc_layout_zipfile = zipfile.ZipFile(osc_layout_file_full_path)

        return osc_layout_zipfile.open(self.osc_zipfile, 'r')
