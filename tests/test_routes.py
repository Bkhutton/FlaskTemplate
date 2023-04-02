import pytest
from flask import Flask, Response, g, session

from flask_app.database.db import get_db

def test_register_blueprint(app: Flask):
    assert len(app.blueprints) > 0

class TestIndex:
    def test_index(self, client):
        response: Response = client.get("/")
        assert response.status_code == 200

class TestAuth:
    def test_register(self, client, app: Flask):
        assert client.get('/auth/register').status_code == 200
        response = client.post(
            '/auth/register', data={'username': 'a', 'password': 'a'}
        )
        assert response.headers["Location"] == "/auth/login"

        with app.app_context():
            assert get_db().execute(
                "SELECT * FROM user WHERE username = 'a'",
            ).fetchone() is not None


    @pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username is required.'),
        ('a', '', b'Password is required.'),
        ('test', 'test', b'already registered'),
    ))
    def test_register_validate_input(self, client, username, password, message):
        response = client.post(
            '/auth/register',
            data={'username': username, 'password': password}
        )
        assert message in response.data

    def test_login(self, client, auth):
        assert client.get('/auth/login').status_code == 200
        response = auth.login()
        assert response.headers["Location"] == "/"

        with client:
            client.get('/')
            assert session['user_id'] == 1
            assert g.user['username'] == 'test'


    @pytest.mark.parametrize(('username', 'password', 'message'), (
        ('a', 'test', b'Incorrect username.'),
        ('test', 'a', b'Incorrect password.'),
    ))
    def test_login_validate_input(self, auth, username, password, message):
        response = auth.login(username, password)
        assert message in response.data

    def test_logout(self, client, auth):
        auth.login()

        with client:
            auth.logout()
            assert 'user_id' not in session