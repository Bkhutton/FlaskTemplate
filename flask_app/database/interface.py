from ..database.db import get_db
from werkzeug.security import generate_password_hash

def register_user(username: str, password: str):
    get_db().execute("INSERT INTO user (username, password) VALUES (?, ?)",
        (username, generate_password_hash(password))
    )
    get_db().commit()

def get_user_by_username(username: str):
    return get_db().execute('SELECT * FROM user WHERE username = ?', 
                      (username,)).fetchone()

def get_user_by_id(id: int):
    return (get_db().execute("SELECT * FROM user WHERE id = ?", 
                            (id,)).fetchone())