from typing import List
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, update
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.db import db
from app.models.ordenCompra import OrdenCompra

class PlanComercial(db.Model, UserMixin):
    __tablename__ = "planComercial"
    id = Column(Integer,primary_key=True)
    idcoleccion = Column(Integer)
    lotes = Column(Integer)
    fechaDeSalida = Column(DateTime)

    def __init__(self, idcoleccion=idcoleccion, lotes=lotes, fechaDeSalida=fechaDeSalida):
        self.idcoleccion = idcoleccion
        self.lotes = lotes
        self.fechaDeSalida = fechaDeSalida

    def crear(idcoleccion, lotes, fechaDeSalida):
        planComercial = PlanComercial(idcoleccion, lotes, fechaDeSalida)
        db.session.add(planComercial)
        db.session.commit()
        return planComercial.id
    
    def existe(idcoleccion):
        if PlanComercial.query.filter_by(idcoleccion=idcoleccion).first():
            return False
        else:
            return True
    
    def ordenesDeComprasListas(idcoleccion):
        if PlanComercial.query.filter_by(idcoleccion=idcoleccion).first():
            idplan = PlanComercial.query.filter_by(idcoleccion=idcoleccion).first().id
            return OrdenCompra.todasListas(idplan)
        else:
            return False