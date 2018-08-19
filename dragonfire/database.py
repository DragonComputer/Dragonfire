#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: database
    :platform: Unix
    :synopsis: the module that contains the database schema of Dragonfire.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    """Schema of `users` table.
    """

    __tablename__ = 'users'
    __table_args__ = {'useexisting': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    gender = Column(String(1), nullable=False)
    birth_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Fact(Base):
    """Schema of `facts` table.
    """

    __tablename__ = 'facts'
    __table_args__ = {'useexisting': True}
    id = Column(Integer, primary_key=True)
    subject = Column(String(255), nullable=False)
    verbtense = Column(String(255), nullable=False)
    clause = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), default=0)
    user = relationship(User)
    is_public = Column(Boolean, default=True)
    counter = Column(Integer, default=1)


class Notification(Base):
    """Schema of `notifications` table.
    """

    __tablename__ = 'notifications'
    __table_args__ = {'useexisting': True}
    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    title = Column(String(63), nullable=False)
    message = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    capitalize = Column(Boolean, default=False)
