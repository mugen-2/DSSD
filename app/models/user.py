import email
from typing import List
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, update
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.db import db



class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(300))
    username = Column(String(100), unique=True)
    area = Column(String(300))
    usernameB = Column(String(100), unique=True)
    passwordB = Column(String(300))

    def __init__(self, first_name=None, last_name=None, email=None, password=None, username=None, area=None, usernameB=None, passwordB=None):
            self.first_name = first_name
            self.last_name = last_name
            self.email = email
            self.password = password
            self.username = username
            self.area = area 
            self.usernameB = usernameB
            self.passwordB = passwordB
        
    def crear(nombre,apellido,email,password,username,areas,usernameB,passwordB):
        user = User(nombre,apellido,email,password,username,areas,usernameB,passwordB)
        db.session.add(user)
        db.session.commit()

    def delete(user):
        db.session.delete(user)
        db.session.commit()

""" def setUserB(user_id,usernameB,passwordB):
        user = User.query.filter_by(id=user_id)
        user.passwordB = passwordB
        user.usernameB = usernameB
        db.session.commit()
 """
