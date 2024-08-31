import os
import sys

from flask import Flask

sys.path.insert(0, 'src/musicsynthesisfinal')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from flaskr import example
    app.register_blueprint(example.bp)

    return app
