import os
import sqlite3
from flask import Flask
import pytest
from flask_app.database.database import get_db
from flask_app.database.database import SQLDatabase
from tests.tests_database.abc_test_database import TestDatabase


class TestSQLDatabase(TestDatabase):

    def setup(self):
        with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
            _data_sql = f.read().decode("utf8")
            get_db().connection.executescript(_data_sql)
    
    def assert_user_exists(self, app: Flask, username: str):
        with app.app_context():
            assert get_db().connection.execute(
                f"SELECT * FROM user WHERE username = '{username}'",
            ).fetchone() is not None


def test_get_close_db(app: Flask):
    with app.app_context():
        db: SQLDatabase = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.connection.execute('SELECT 1')

    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flask_app.database.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called

def test_create_user_table(app: Flask):
    with app.app_context():
        db: SQLDatabase = get_db()
        db.connection.execute('SELECT * FROM user').fetchall()