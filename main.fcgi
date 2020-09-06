#!/home1/anyoneil/public_html/labelchopper/env/bin/python

from sys import path
from flup.server.fcgi import WSGIServer

path.insert(0, '/home/anyoneil/public_html/labelchopper/')
from labelizer import app, socketio

if __name__ == '__main__':
    WSGIServer(app).run()
