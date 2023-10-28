from wtforms import ValidationError

from flask_app.database.database import get_db

class Unique(object):
    def __init__(self, table, field, message=None):
        self.table = table
        self.field = field
        if not message:
            message = 'Already used.'
        self.message = message
        
    def __call__(self, form, field):
        if get_db().test_if_unique(self.table, self.field, field.data):
            raise ValidationError(self.message)