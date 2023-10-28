import sqlite3

from flask import current_app, g
from werkzeug.security import generate_password_hash

from flask_app.database.abc_database import Database

class SQLDatabase(Database):

    def __init__(self):
        self.connection = sqlite3.connect(current_app.config['DATABASE'])
        self.connection.row_factory = sqlite3.Row

    def setup(self):
        with current_app.open_resource('database/schema.sql') as f:
            self.connection.executescript(f.read().decode('utf-8'))
   
    def register_user(self, username: str, password: str):
        self.connection.execute("INSERT INTO user (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        self.connection.commit()

    def get_user_by_username(self, username: str):
        return self.connection.execute('SELECT * FROM user WHERE username = ?', 
                        (username,)).fetchone()

    def get_user_by_id(self, id: int):
        return (self.connection.execute("SELECT * FROM user WHERE id = ?", 
                                (id,)).fetchone())
    
    def test_if_unique(self, table, field, data):
        query = f"SELECT * FROM {table} WHERE {field} = '{data}'"
        query = f"SELECT * FROM {table} WHERE {field} = ?"
        if self.connection.execute(query, (data,)).fetchone() is not None:
            return True
        return False
    
    def close_db(self, e=None):
        g.pop('db', None)
        self.connection.close()