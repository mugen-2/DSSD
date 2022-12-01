from typing import List
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, update
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.db import db

class Importacion(db.Model, UserMixin):
    __tablename__ = "importacion"
    id = Column(Integer,primary_key=True)
    codigop = Column(String)
    direccion = Column(String)
    idColeccion = Column(Integer)

    def __init__(self, codigop=None, direccion=None, idColeccion=None):
        self.codigop=codigop
        self.direccion=direccion
        self.idColeccion=idColeccion

    def crear(codigop, direccion, idColeccion):
        importacion = Importacion(codigop, direccion, idColeccion)
        db.session.add(importacion)
        db.session.commit()