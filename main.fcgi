#!/home1/anyoneil/public_html/labelchopper/env/bin/python
from wsgiref.handlers import CGIHandler
from werkzeug.middleware.proxy_fix import ProxyFix
from flup.server.fcgi import WSGIServer

from sys import path
path.insert(0, '/home/anyoneil/public_html/labelchopper/')
from labelizer import app

if __name__ == '__main__':
    WSGIServer(app).run()
