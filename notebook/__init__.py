from flask import Flask
from os import makedirs
from .config import init_config
from .db import init_db
from .routes import init_routes

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    init_config(app)

    init_db(app)
    
    # Register application routes and error handlers (blueprints)
    init_routes(app)

    return app