from SocketServer import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, make_server

import bottle
import json
import os

import sessions
import password


@bottle.route('/')
@bottle.view('login')
@sessions.start
def login_page(session):
    if session.get('in'):
        bottle.redirect('/index')
    return {}


@bottle.route('/', method='POST')
@sessions.start
def process_login(session):
    if session.get('in'):
        bottle.redirect('/index')

    p = bottle.request.forms.get('password')
    with open('config.json') as f:
        passw, salt = json.load(f)['password']
    hashed = password.encrypt(p, salt)[0]
    if hashed == passw:
        session['in'] = True
        bottle.redirect('/index')
    bottle.redirect('/')


@bottle.route('/index')
@bottle.view('index')
@sessions.start
def serve_index(session):
    if not session.get('in'):
        bottle.redirect('/')

    files = os.listdir('pads/')
    files.sort(key=lambda f: os.stat(os.path.join('pads', f)).st_mtime, reverse=True)
    return {'files': files}


@bottle.route('/p/<pad>')
@bottle.view('editor')
@sessions.start
def pad_editor(session, pad):
    if not session.get('in'):
        bottle.redirect('/')

    path = 'pads/{0}.md'.format(pad)
    response = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            response['data'] = f.read().replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        with open('config.json') as f:
            published = json.load(f)['published']
        response['published'] = pad in published

    else:
        response['data'] = ''
        response['published'] = False

    return response


@bottle.route('/p/<pad>/save', method='POST')
@sessions.start
def save_pad(session, pad):
    if not session.get('in'):
        return 'You are not logged in, or your session expired!'

    data = bottle.request.forms.get('data')
    path = 'pads/{0}.md'.format(pad)
    if data is not None:
        with open(path, 'w') as f:
            f.write(data)
        return 'The operation succeeded!'
    return 'The operation failed!'


@bottle.route('/p/<pad>/rename/<newpad>')
@sessions.start
def rename_pad(session, pad, newpad):
    if not session.get('in'):
        return 'You are not logged in, or your session expired!'

    oldpath = 'pads/{0}.md'.format(pad)
    newpath = 'pads/{0}.md'.format(newpad)
    if not os.path.exists(newpath) and os.path.exists(oldpath):
        with open(oldpath, 'r') as f_in:
            with open(newpath, 'w') as f_out:
                f_out.write(f_in.read())
        os.unlink(oldpath)
        return 'The operation succeeded!'
    return 'The operation failed!'


@bottle.route('/p/<pad>/delete')
@sessions.start
def delete_pad(session, pad):
    if not session.get('in'):
        bottle.redirect('/')

    path = 'pads/{0}.md'.format(pad)
    if os.path.exists(path):
        os.unlink(path)
    bottle.redirect('/index')


@bottle.route('/logout')
@sessions.start
def logout(session):
    sessions.destroy()
    bottle.redirect('/')


@bottle.route('/static/<filename>')
def serve_static(filename):
    return bottle.static_file(filename, root='./views/static')


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
