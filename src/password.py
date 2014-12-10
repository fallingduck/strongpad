import scrypt
import os
import binascii


def encrypt(password, salt=None):
    if salt is None:
        salt = os.urandom(8)
    hashed = scrypt.hash(password, salt)
    return binascii.hexlify(hashed), binascii.hexlify(salt)
