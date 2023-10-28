import pytest
import tempfile
import os
from flask_app import create_app
from flask_app.database.database import init_db
import config
from tests.tests_database.test_sql_database import TestSQLDatabase


@pytest.fixture()
def app():
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    conf = config.TestConfig
    conf.DATABASE = db_path
    app = create_app(config=config.TestConfig)
    # other setup can go here
    with app.app_context():
        init_db()
        test_db = TestSQLDatabase()
        test_db.setup()

    yield app

    # clean up / reset resources here
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


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