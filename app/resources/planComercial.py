from concurrent.futures import process
from email import header
from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
from app.forms.planComercial_form import Form_planComercial_new
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user
from app.models.planComercial import PlanComercial
from app.models.ordenCompra import OrdenCompra
import requests
import json
import random

def new(idcoleccion):
    form = Form_planComercial_new()
    return render_template("planComercial/new.html", form=form, idcoleccion=idcoleccion) 

def create(idcoleccion):
    form = Form_planComercial_new()    
    if (form.validate_on_submit()):
        fechaDeSalida = request.form.get("fechaDeSalida")
        lotes = request.form.get("lotes")
        lotes = int(lotes)

        ordenes = random.randint(1, lotes)

        idplancomercial = PlanComercial.crear(idcoleccion, lotes, fechaDeSalida)

        for i in range(ordenes):
            orden = random.randint(1000000000, 9999999999)
            OrdenCompra.crear(idplancomercial, orden)
        

        return redirect(url_for("collection_index"))
    return render_template("planComercial/new.html", form=form, idcoleccion=idcoleccion)      