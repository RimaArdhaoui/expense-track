import os
from flask import Flask

from .config import Config
from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    return app
