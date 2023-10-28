import flask

from .index import index_bp
from .auth import auth_bp


def init_app(app: flask.Flask):
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
