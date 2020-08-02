import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        "something-for-debugging-only-6544#]`()!)54543qqwdqw1112vm"
    UPLOAD_FOLDER = 'upload'
    OUTPUT_FOLDER = 'output'
    ALLOWED_EXTENSIONS = {'pdf'}
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
