from typing import List
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, update
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.db import db

class Collection(db.Model, UserMixin):
    __tablename__ = "collections"
    id = Column(Integer,primary_key=True)
    nombre = Column(String(100), unique=True)
    tipo = Column(String(100))
    plazoF = Column(Integer)
    fechaL = Column(DateTime)
    adicional = Column(String(300))
    #google=Column(TINYINT)

    def __init__(self, nombre=None, tipo=None, plazoF=None, fechaL=None, adicional=None):
        self.nombre = nombre
        self.tipo = tipo
        self.plazoF = plazoF
        self.fechaL = fechaL
        self.adicional = adicional

    def crear(nombre, tipo, plazoF, fechaL, adicional):
        collection= Collection(nombre,tipo,plazoF,fechaL,adicional)
        db.session.add(collection)
        db.session.commit()