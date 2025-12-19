from flask import Blueprint

bp = Blueprint('search', __name__, url_prefix='/search')


@bp.route('/title', methods=['POST'])
def search_by_title():
    pass


@bp.route('/content', methods=['POST'])
def search_by_content():
    pass


@bp.route('/tags', methods=['POST'])
def search_by_tags():
    pass


@bp.route('/hisotry')
def search_history():
    pass


@bp.route('/history/<int:history_id>/delete', methods=['POST'])
def delete_search_history(history_id):
    pass