import functools
from json import dumps

from flask import (Blueprint, g, redirect, render_template, request, session,
                   url_for)
from resumake.db import get_db
from resumake.models import User
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/signin', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('index'))

        return render_template('auth/signin.html', error=error)

    return render_template('auth/signin.html')


@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        error = None
        db = get_db()
        user = User(signup=True)

        if password != confirm:
            error = 'Entered passwords don\'t match'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password_hash, resume_data) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), dumps(user.data))
            )
            db.commit()

            return redirect(url_for('auth.signin'))

        return render_template('auth/signup.html', error=error)

    return render_template('auth/signup.html')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@auth_bp.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.signin'))

        return view(**kwargs)

    return wrapped_view
