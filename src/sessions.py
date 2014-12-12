'''The unofficial Sessions addon for Bottle (bottlepy.org)
Made by Magnie Mozios and Falling Duck
License: MIT


Usage:

from sessions import start, destroy

@route('/')
@start
def home(session):
    # session is a dict that can be read from and written to
    destroy()  # the module knows which session to delete automatically
'''


__version__ = '2.0'


from os import urandom
from hashlib import sha1
from bottle import request, response
from collections import defaultdict
from time import time
from binascii import hexlify


_data = defaultdict(dict)


def start(func):
    'Creates a new session or accesses an existing one.'

    def wrapper(*a, **k):
        if request.get_cookie('PYSESSID') is None:
            sid = hexlify(urandom(32))
            response.set_cookie('PYSESSID', sid)
            sid = sha1('%s%s' % (sid, request['REMOTE_ADDR'])).hexdigest()
            _data[sid]['__date'] = int(time()) + 1800
        else:
            sid = request.get_cookie('PYSESSID')
            sid = sha1('%s%s' % (sid, request['REMOTE_ADDR'])).hexdigest()

        for ssid in dict(_data):
            if _data[ssid]['__date'] < time():
                del _data[ssid]

        _data[sid]['__date'] = int(time()) + 3600

        return func(_data[sid], *a, **k)
    return wrapper


def destroy():
    'Destroys the session of the current user.'
    try:
        sid = request.get_cookie('PYSESSID')
        sid = sha1('%s%s' % (sid, request['REMOTE_ADDR'])).hexdigest()
        del _data[sid]
    except Exception:
        pass
