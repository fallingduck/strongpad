# strongpad

> With a simplistic interface that lets you hand-craft your next manifesto from anywhere in the world using markdown, strongpad packs a powerful punch, despite its minimalism.

> &mdash; <cite>Me</cite>

Software like Etherpad is designed mainly for collaborative editing. These projects end up essentially as real-time wikis. Strongpad takes a different approach. Strongpad is your virtual bedroom. Using strongpad, you write in private, as an individual. Your strongpad instance is protected by a password, so only you can write using it. If you want to share one of your documents with a friend, strongpad can make it available for viewing, but not for editing. You can make a document private again at any time.

---

To install:

```
$ sudo pip2 install bottle scrypt

$ git clone https://github.com/fallingduck/strongpad.git

$ cd strongpad

$ python2 strongpad.py
```

The first time you start strongpad up, it will ask you to set a password. This password will be needed every time you log into the server from the web interface. To change this password at any time, you can run:

`$ python2 strongpad.py password`

And it will prompt you for a new password.

Now navigate to `http://localhost:3031` and sign in!

When exposing strongpad to the internet, it is highly recommended that you use TLS for privacy while you're writing.
