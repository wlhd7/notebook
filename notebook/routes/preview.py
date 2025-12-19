from flask import Blueprint

bp = Blueprint('preview', __name__, url_prefix='/preview')


@bp.route('/')
def index():
    return 'hello'