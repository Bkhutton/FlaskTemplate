from wtforms import Form, StringField, PasswordField, BooleanField, validators

from .validators.unique import Unique

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired(message='Username required.'), Unique('user', 'username', message='Username is already registered.')])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired('Email required.')])
    password = PasswordField('New Password', [
        validators.DataRequired(message='Password Required.'),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])