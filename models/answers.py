"""Answer model"""
from sqlalchemy import Column, Integer, String
from db import BASE


class Answer(BASE):  # pylint: disable=too-few-public-methods
    """ Answer model """
    __tablename__ = 'answer'
    id = Column(Integer(), primary_key=True)
    reply = Column(String(200), nullable=False)
    user_id = Column(Integer(), nullable=False)
    form_id = Column(Integer(), nullable=False)
    field_id = Column(Integer(), nullable=False)
    group_id = Column(Integer(), nullable=False)
