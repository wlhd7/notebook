from flask import Blueprint

bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/')
def index():
    pass