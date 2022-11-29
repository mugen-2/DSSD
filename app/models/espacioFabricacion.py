from typing import List
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, update
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.db import db

class EspacioFabricacion(db.Model, UserMixin):
    __tablename__ = "espacioFabricacion"
    id = Column(Integer,primary_key=True)
    idcoleccion = Column(Integer)
    idreserva = Column(Integer)
    estado = Column(String(100))

    def __init__(self, idreserva = idreserva, idcoleccion=idcoleccion):
        self.idreserva = idreserva
        self.idcoleccion = idcoleccion
        self.estado = "no"

    def crear(idreserva, idcoleccion):
        espacioFabricacion = EspacioFabricacion(idreserva,idcoleccion)
        db.session.add(espacioFabricacion)
        db.session.commit()

    def tieneEspacioFabricacion(idC):
        return EspacioFabricacion.query.filter_by(idcoleccion=idC).first()
    
    def entregado(idreserva):
        reserva = EspacioFabricacion.query.filter_by(idreserva=idreserva).first()
        reserva.estado = "si"
        db.session.commit()