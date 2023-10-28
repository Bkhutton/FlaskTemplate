from flask import Flask


def test_config(app: Flask):
    assert app.config.get("SECRET_KEY") == 'test'
    assert app.config.get("TESTING") is True
    assert app.config.get("SQLALCHEMY_DATABASE_URI") == 'sqlite:///:memory:'
