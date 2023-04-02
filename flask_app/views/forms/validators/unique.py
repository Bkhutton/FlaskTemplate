from wtforms import ValidationError

from flask import current_app
from flask_app.database.db import get_db

class Unique(object):
    def __init__(self, table, field, message=None):
        self.table = table
        self.field = field
        if not message:
            message = 'Already used.'
        self.message = message
        
    def __call__(self, form, field):
        with current_app.app_context():
            query = f"SELECT * FROM {self.table} WHERE {self.field} = '{field.data}'"
            query = f"SELECT * FROM {self.table} WHERE {self.field} = ?"
            if get_db().execute(query, (field.data,)).fetchone() is not None:
                raise ValidationError(self.message)