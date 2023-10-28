import os
from flask import Flask

from . import models
from . import views
from config import DevConfig


def create_app(config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(DevConfig)
    views.init_app(app)
    models.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
