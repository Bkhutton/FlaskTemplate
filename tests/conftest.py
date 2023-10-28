import pytest
from flask_app import create_app
import config
from flask_app.models.base import db
from flask_app.models.user import User


@pytest.fixture()
def app():
    app = create_app(config=config.TestConfig)
    # other setup can go here
    with app.app_context():
        _popualte_database()

    yield app

    # clean up / reset resources here
    with app.app_context():
        db.drop_all()


def _popualte_database():
    user = User(username="test",
                email="first_user@gmail.com",
                password=('pbkdf2:sha256:50000$TCI4GzcX'
                          '$0de171a4f4dac32e3364c7ddc7c'
                          '14f3e2fa61f2d17574483f7ffbb431b4acb2f'))
    db.session.add(user)
    db.session.commit()


@pytest.fixture()
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
