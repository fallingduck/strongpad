from SocketServer import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, make_server

import bottle
import sessions


@bottle.error(404)
@bottle.error(403)
@bottle.error(401)
@bottle.error(500)
def error_page(e):
    return 'Error!'


class ThreadingWSGIServer(WSGIServer, ThreadingMixIn):
    pass


def start(host='localhost', port=3031):
    server = make_server(host, port, bottle.default_app(), ThreadingWSGIServer)
    print 'Serving on http://{0}:{1}...'.format(host, port)
    server.serve_forever()
