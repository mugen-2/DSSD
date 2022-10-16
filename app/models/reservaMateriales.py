from typing import List
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, update
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.db import db

class ReservaMateriales(db.Model, UserMixin):
    __tablename__ = "reservaMateriales"
    id = Column(Integer,primary_key=True)
    idcoleccion = Column(Integer)
    nombre = Column(String(100))
    cantidad = Column(Integer)
    #google=Column(TINYINT)

    def __init__(self, nombre=None, cantidad=None, idcoleccion=idcoleccion):
        self.nombre = nombre
        self.cantidad = cantidad
        self.idcoleccion = idcoleccion

    def crear(nombre, cantidad, idcoleccion):
        reservaMateriales= ReservaMateriales(nombre,cantidad,idcoleccion)
        db.session.add(reservaMateriales)
        db.session.commit()