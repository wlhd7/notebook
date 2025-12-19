from flask import Blueprint, request, session, redirect, url_for, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
from ..db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def _get_user_by_username(username: str) -> Optional[dict]:
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT id, username, password_hash FROM users WHERE username=%s", (username,))
        return cur.fetchone()


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form.to_dict()
        username = (data.get('username') or '').strip()
        password = data.get('password') or ''

        if not username or not password:
            if 'application/json' in request.headers.get('Accept', ''):
                return jsonify({'error': 'username and password required'}), 400
            return render_template('auth/login.html', error='username and password required'), 400

        user = _get_user_by_username(username)
        if user is None or not check_password_hash(user['password_hash'], password):
            if 'application/json' in request.headers.get('Accept', ''):
                return jsonify({'error': 'invalid credentials'}), 401
            return render_template('auth/login.html', error='invalid credentials'), 401

        # Authentication successful; set session
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']

        if 'application/json' in request.headers.get('Accept', ''):
            return jsonify({'message': 'logged_in', 'user': user['username']}), 200

        return redirect(url_for('preview.index'))

    return render_template('auth/login.html')


@bp.route('/logout', methods=('POST',))
def logout():
    user = session.pop('username', None)
    session.pop('user_id', None)
    if 'application/json' in request.headers.get('Accept', ''):
        return jsonify({'message': 'logged_out', 'user': user}), 200
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form.to_dict()
        username = (data.get('username') or '').strip()
        password = data.get('password') or ''

        if not username or not password:
            if 'application/json' in request.headers.get('Accept', ''):
                return jsonify({'error': 'username and password required'}), 400
            return render_template('auth/register.html', error='username and password required'), 400

        # Ensure user does not already exist
        if _get_user_by_username(username) is not None:
            if 'application/json' in request.headers.get('Accept', ''):
                return jsonify({'error': 'username already taken'}), 409
            return render_template('auth/register.html', error='username already taken'), 409

        password_hash = generate_password_hash(password)
        db = get_db()
        with db.cursor() as cur:
            cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
            # rely on autocommit=True in get_db()

        if 'application/json' in request.headers.get('Accept', ''):
            return jsonify({'message': 'registered', 'user': username}), 201

        return render_template('auth/register.html', success=True, user=username)

    return render_template('auth/register.html')