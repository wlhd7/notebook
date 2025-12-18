from flask import Flask
from os import makedirs
from .config import init_config

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    init_config(app)
