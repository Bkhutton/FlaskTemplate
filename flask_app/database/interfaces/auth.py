from werkzeug.security import generate_password_hash
from db import get_db

def create_user(username, password):
    db = get_db()
    try:
        db.execute('INSERT INTO user (username, password) VALUES (?, ?)', username, generate_password_hash(password))
        db.commit()
    except db.IntegrityError:
        return f'User {username} is already registered.'