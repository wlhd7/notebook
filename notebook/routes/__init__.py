from .preview import bp as preview
from .search import bp as search
from .notes import bp as notes
from .tags import bp as tags
from .errors import not_found

bps = [preview, search, notes, tags]


def init_routes(app):
    for bp in bps:
        app.register_blueprint(bp)

    # Register a global 404 handler from the errors module
    app.register_error_handler(404, not_found)