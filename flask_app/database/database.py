import click
from flask import Flask, g
from flask_app.database.abc_database import Database

from flask_app.database.implementations.mysql_database import SQLDatabase

def get_db() -> Database:
    if 'db' not in g:
        g.db = SQLDatabase()
    return g.db

def close_db(e=None):
    if e:
        raise e
    get_db().close_db()

def init_db():
    g.db = SQLDatabase()
    g.db.setup()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized database.')

def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)