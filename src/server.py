from SocketServer import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, make_server

import bottle
import json
import os
import markdown2

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
        bottle.redirect('/p/{0}/'.format(pad))

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


@bottle.route('/p/<pad>/')
@bottle.view('viewer')
@sessions.start
def pad_viewer(session, pad):
    with open('config.json', 'r') as f:
        published = json.load(f)['published']
    if pad in published:
        path = 'pads/{0}.md'.format(pad)
        with open(path, 'r') as f:
            return {'data': f.read().replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')}
    elif session.get('in'):
        bottle.redirect('/p/{0}'.format(pad))
    else:
        bottle.redirect('/')


@bottle.route('/p/<pad>/<mode:re:(md|html)>')
@sessions.start
def md_viewer(session, pad, mode):
    with open('config.json', 'r') as f:
        published = json.load(f)['published']
    if pad in published or session.get('in'):
        path = 'pads/{0}.md'.format(pad)
        if mode == 'html':
            return markdown2.markdown_path(path)
        else:
            with open(path, 'r') as f:
                bottle.response.content_type = 'text/plain'
                return f.read()
    else:
        bottle.abort(404)


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


@bottle.route('/p/<pad>/rename/<newpad>', method='POST')
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
        with open('config.json', 'r') as f:
            config = json.load(f)
        if pad in config['published']:
            config['published'].remove(pad)
            config['published'].append(newpad)
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
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
    with open('config.json', 'r') as f:
        config = json.load(f)
    if pad in config['published']:
        config['published'].remove(pad)
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    bottle.redirect('/index')


@bottle.route('/p/<pad>/publish', method='POST')
@sessions.start
def publish_pad(session, pad):
    if not session.get('in'):
        return 'You are not logged in, or your session expired!'

    with open('config.json', 'r') as f:
        config = json.load(f)
    if pad not in config['published']:
        config['published'].append(pad)
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    return 'This pad is now available for viewing!'


@bottle.route('/p/<pad>/unpublish', method='POST')
@sessions.start
def unpublish_pad(session, pad):
    if not session.get('in'):
        return 'You are not logged in, or your session expired!'

    with open('config.json', 'r') as f:
        config = json.load(f)
    if pad in config['published']:
        config['published'].remove(pad)
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    return 'This pad is no longer available for viewing!'


@bottle.route('/logout')
@sessions.start
def logout(session):
    sessions.destroy()
    bottle.redirect('/')


@bottle.route('/static/<filename>')
def serve_static(filename):
    return bottle.static_file(filename, root='./views/static')


@bottle.error(404)
def not_found(e):
    return '404: Not Found'


@bottle.error(403)
def forbidden(e):
    return '403: Forbidden'


@bottle.error(500)
def server_error(e):
    return '500: Internal Server Error'


class ThreadingWSGIServer(WSGIServer, ThreadingMixIn):
    pass


def start(host='localhost', port=3031):
    server = make_server(host, port, bottle.default_app(), ThreadingWSGIServer)
    print 'Serving on http://{0}:{1}...'.format(host, port)
    server.serve_forever()
