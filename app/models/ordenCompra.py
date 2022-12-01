from typing import List
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean, update
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app.db import db

class OrdenCompra(db.Model, UserMixin):
    __tablename__ = "ordenCompra"
    id = Column(Integer,primary_key=True)
    idplancomercial = Column(Integer)
    orden = Column(String)
    verificado = Column(Boolean)

    def __init__(self, idplancomercial=idplancomercial, orden=orden):
        self.idplancomercial = idplancomercial
        self.orden = orden
        self.verificado = False

    def crear(idplancomercial, orden):
        ordenCompra = OrdenCompra(idplancomercial, orden)
        db.session.add(ordenCompra)
        db.session.commit()

    def actualizar(idorden):
        ok = OrdenCompra.query.filter_by(orden=idorden).first()
        ok.verificado = True
        db.session.commit()