from typing import List
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, update
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

    def __init__(self, idplancomercial=idplancomercial, orden=orden):
        self.idplancomercial = idplancomercial
        self.orden = orden

    def crear(idplancomercial, orden):
        ordenCompra = OrdenCompra(idplancomercial, orden)
        db.session.add(ordenCompra)
        db.session.commit()