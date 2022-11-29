from typing import List
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, update
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.db import db

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