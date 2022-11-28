from typing import List
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, update, Boolean
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
    estado = Column(String(100))

    def __init__(self, idreserva = idreserva, idcoleccion=idcoleccion):
        self.idreserva = idreserva
        self.idcoleccion = idcoleccion
        self.estado = "no"

    def crear(idreserva, idcoleccion):
        reservaMateriales = ReservaMateriales(idreserva,idcoleccion)
        db.session.add(reservaMateriales)
        db.session.commit()
    
    def entregado(idreserva):
        reserva = ReservaMateriales.query.filter_by(idreserva=idreserva).first()
        reserva.estado = "si"
        db.session.commit()

    def reservasPorColeccion(idcoleccion):
        return ReservaMateriales.query.filter_by(idcoleccion=idcoleccion).all()

    def terminaronTodasReservas(idcoleccion):
        aux = True
        reservas = ReservaMateriales.query.filter_by(idcoleccion=idcoleccion).all()
        for reserva in reservas:
            if reserva.estado != "si":
                aux = False
        return aux