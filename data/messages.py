import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin



class Message(SqlAlchemyBase, UserMixin):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    sender_name = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String)
    time = sqlalchemy.Column(sqlalchemy.DateTime)
    user = orm.relationship('User')