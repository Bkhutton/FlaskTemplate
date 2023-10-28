from sqlalchemy import Integer
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from .base import db


class User(db.Model):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(15), nullable=False, unique=True)
    email = Column(String(50), nullable=True, unique=True)
    password = Column(String(256), nullable=True)


def register_user(username: str, email: str, password: str):
    db.session.add(User(username=username, email=email, password=password))
    db.session.commit()


def get_user_by_username(username: str):
    return User.query.filter_by(username=username).first()


def get_user_by_id(id: int):
    return User.query.filter_by(id=id).first()
