# strongpad

A solution for simple, private, and portable remote document editing.

---

Strongpad uses markdown for client side formatting. It is served with the Bottle microframework using a standard library threaded WSGI server. Client-server communication is done using AJAX. (These are mostly notes for myself).

To install:

```
$ pip2 install bottle scrypt

$ git clone https://github.com/fallingduck/strongpad.git

$ cd strongpad

$ python2 strongpad.py
```

The first time you start strongpad up, it will ask you to set a password. This password will be needed every time you log into the server from the web interface. To change this password at any time, you can run:

`$ python2 strongpad.py password`

And it will prompt you for a new password.

Now navigate to `http://localhost:3031` and sign in!

When exposing strongpad to the internet, it is highly recommended that you use TLS for privacy while you're writing.
