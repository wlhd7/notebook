from os import environ

def init_config(app):
    # Start with an empty mapping, allow instance/config.py to override
    app.config.from_mapping()

    # Load the instance config (untracked, environment-specific)
    app.config.from_pyfile('config.py', silent=True)

    # Allow environment variables to override instance config
    if environ.get('DB_HOST'):
        app.config['DB_HOST'] = environ['DB_HOST']

    if environ.get('DB_PORT'):
        try:
            app.config['DB_PORT'] = int(environ['DB_PORT'])
        except ValueError:
            app.config['DB_PORT'] = 