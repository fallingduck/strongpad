#!/usr/bin/env python2

__author__ = 'Jack VanDrunen'
__version__ = 'pre-alpha'
__license__ = 'MIT'


import json
import os
import sys
import getpass

import src.password


def change_password(config={}):
    password = getpass.getpass(prompt='Enter new password: ')
    if getpass.getpass(prompt='Confirm password: ') != password:
        print 'Passwords did not match!'
        sys.exit(1)
    hashed, salt = src.password.encrypt(password)

    config['password'] = [
        hashed,
        salt
    ]

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)


if __name__ == '__main__':
    if not os.path.exists('pads'):
        os.mkdir('pads')

    if not os.path.exists('config.json'):
        change_password()
        print 'Password set!'

    elif len(sys.argv) > 1 and sys.argv[1] == 'password':
        with open('config.json', 'r') as f:
            config = json.load(f)
        change_password(config)
        print 'Password changed!'
        sys.exit(0)
