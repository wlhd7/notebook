from .preview import bp as preview
from .search import bp as search
from .notes import bp as notes
from .tags import bp as tags
from .auth import bp as auth
from .errors import not_found
from flask import request, redirect, url_for, session

bps = [preview, search, notes, tags, auth]

def init_routes(app):
    for bp in bps:
        app.register_blueprint(bp)

    app.add_url_rule('/', endpoint='notes.index')

    # Register a global 404 handler from the errors module
    app.register_error_handler(404, not_found)

    # Enforce login for all endpoints by default, with an allowlist.
    # Order of allowlist resolution: `AUTH_PUBLIC_ENDPOINTS` from config -> defaults
    @app.before_request
    def enforce_login():
        endpoint = request.endpoint
        if endpoint is None:
            return  # Ignore requests with no endpoint (e.g., static files)
        
        # Default allowlist of public endpoints
        default_allowlist = {'auth.login', 'auth.register', 'errors.not_found', 'static'}

        # Merge configured public endpoints 
        allowlist = set(app.config.get('AUTH_PUBLIC_ENDPOINTS', [])) | default_allowlist

        if endpoint in allowlist:
            return  # Public endpoint; no login required
        
        if session.get('user_id') is None:
            return redirect(url_for('auth.login', next=request.url))
