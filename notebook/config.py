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
            app.config['DB_PORT'] = app.config.get('DB_PORT', 3306)  # default port if conversion fails

    if environ.get('DB_USER'):
        app.config['DB_USER'] = environ['DB_USER']

    if environ.get('DB_PASSWORD'):
        app.config['DB_PASSWORD'] = environ['DB_PASSWORD']

    if environ.get('DB_NAME'):
        app.config['DB_NAME'] = environ['DB_NAME']

    # Allow SECRET_KEY to be provided via instance config or overridden by environment variable
    if environ.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = environ['SECRET_KEY']

    app.config.setdefault('SECRET_KEY', 'dev')  # default for development if not set

    # sane defaults for non-secret values
    app.config.setdefault('DB_PORT', 3306)
    app.config.setdefault('DB_HOST', 'localhost')
    app.config.setdefault('DB_NAME', 'notebook')

    # Allow setting public endpoints via environment as comma-separated values
    # e.g. AUTH.PUBLIC_ENDPOINTS=auth.login,auth.register,static
    auth_public = environ.get('AUTH.PUBLIC_ENDPOINTS')
    if auth_public:
        app.config['AUTH.PUBLIC_ENDPOINTS'] = [ep.strip() for ep in auth_public.split(',') if ep.strip()]
