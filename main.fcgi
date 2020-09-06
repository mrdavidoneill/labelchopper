#!/home1/anyoneil/public_html/labelchopper/env/bin/python

from sys import path
path.insert(0, '/home/anyoneil/public_html/labelchopper/')
from labelizer import app, socketio

if __name__ == '__main__':
    socketio(run).app()
