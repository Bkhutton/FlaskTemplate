from sqlalchemy import text
from wtforms import ValidationError
from flask_app.models.base import db


class Unique(object):
    def __init__(self, table, field, message=None):
        self.table = table
        self.field = field
        if not message:
            message = 'Already used.'
        self.message = message

    def __call__(self, form, field):
        result = db.session.execute(text(f"SELECT * FROM {self.table} WHERE "
                                         f"{self.field} = '{field.data}'"))
        if result.first() is not None:
            raise ValidationError(self.message)
