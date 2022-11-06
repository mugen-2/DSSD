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
    idreserva = Column(Integer)

    def __init__(self, idreserva = idreserva, idcoleccion=idcoleccion):
        self.idreserva = idreserva
        self.idcoleccion = idcoleccion

    def crear(idreserva, idcoleccion):
        reservaMateriales= ReservaMateriales(idreserva,idcoleccion)
        db.session.add(reservaMateriales)
        db.session.commit()