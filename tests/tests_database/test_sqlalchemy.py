from flask import Flask
import pytest
from sqlalchemy import inspect

from flask_app.models.base import db


class TestSQLAlchemy():

    def test_db_exists(self):
        assert db is not None

    def test_tables_created(self):
        self._assert_table_exists(name="User")

    @pytest.fixture(autouse=True)
    def _get_app(self, app: Flask):
        self._app = app

    def _assert_table_exists(self, name: str):
        with self._app.app_context():
            assert inspect(db.engine).has_table(name)
