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
    #google=Column(TINYINT)

    def __init__(self, first_name=None, last_name=None, email=None, password=None, username=None, area=None, google=None):
            self.first_name = first_name
            self.last_name = last_name
            self.email = email
            self.password = password
            self.username = username
            self.area = area 
            #self.google=google
        
    def crear(nombre,apellido,email,password,username,areas):
        user = User(nombre,apellido,email,password,username,areas)
        db.session.add(user)
        db.session.commit()

    def delete(user):
        db.session.delete(user)
        db.session.commit()


