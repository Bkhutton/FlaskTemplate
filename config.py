class Config(object):
    TESTING = False

class TestConfig(Config):
    TESTING = True
    SECRET_KEY = 'test'
    DATABASE = ''

class DevConfig(Config):
    SECRET_KEY = 'dev'
    DATABASE = 'flask_app.sqlite'
