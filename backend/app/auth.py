from flask import (
    Blueprint, request, g, abort
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from flask_httpauth import HTTPBasicAuth
import json
from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
basicauth = HTTPBasicAuth()

@bp.route('/register', methods=['POST'])
def authorize():
    username = request.form['username']
    password = request.form['password']

    if username is None or password is None:
        abort(400)
    
    db = get_db()
    if db.execute(
        'SELECT id FROM user WHERE username = ?',
        (username,),
    ).fetchone() is not None:
        abort(400)
    
    db.execute(
        'INSERT INTO user(username, password)'
        'VALUES(?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()

    return json.dumps({'success': True, 'user': username})

@basicauth.verify_password
def verify_password(username, password):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username = ?',
        (username,),
    ).fetchone()
    if user and check_password_hash(user['password']):
        return True
    return False
