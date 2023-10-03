import os
from flask import Flask

from .blueprints import index, about, map, data, models


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    app.register_blueprint(index.bp)
    app.register_blueprint(about.bp)
    app.register_blueprint(map.bp)
    app.register_blueprint(data.bp)
    # app.register_blueprint(models.bp)

    return app
