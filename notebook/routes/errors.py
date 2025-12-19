from flask import Blueprint, jsonify, render_template, request

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(404)
def not_found(error):
    """Handle 404 errors.

    Returns JSON when the client accepts JSON; otherwise attempts to
    render `404.html` and falls back to a plain text response.
    """
    accept = request.headers.get('Accept', '')
    if 'application/json' in accept:
        return jsonify({'error': 'Not Found', 'code': 404}), 404

    try:
        return render_template('404.html'), 404
    except Exception:
        return '404 Not Found', 404