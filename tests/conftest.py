import pytest
import tempfile
import os
from flask_app import create_app
from flask_app.database.db import init_db, get_db
import config

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")

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
        get_db().executescript(_data_sql)

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