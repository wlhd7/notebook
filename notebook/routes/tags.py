from flask import Blueprint

bp = Blueprint('tags', __name__, url_prefix='/tags')


@bp.route('/')
def index():
    pass


@bp.route('/<int:tag_id>/add', methods=['POST'])
def add_tag(tag_id):
    pass


@bp.route('/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    pass


@bp.route('/<int:tag_id>/rename', methods=['POST'])
def rename_tag(tag_id):
    pass