from concurrent.futures import process
from email import header
from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
from app.forms.espacioFabricacion_form import Form_espacioFabricacion_new
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user
from app.models.espacioFabricacion import EspacioFabricacion
import requests
import json

def index(idcoleccion):
    response = requests.get("https://dssdapi.fly.dev/api/listarf/")
    espaciosFabricacion = response.json()["fabricantes"][0]
    return render_template("espacioFabricacion/index.html",espaciosFabricacion=espaciosFabricacion, idcoleccion=idcoleccion)

def new(idcoleccion, idfabricante):
    form = Form_espacioFabricacion_new()
    return render_template("espacioFabricacion/new.html", form=form, idcoleccion=idcoleccion, idfabricante=idfabricante) 

def create(idcoleccion, idfabricante):
    form = Form_espacioFabricacion_new()    
    if (form.validate_on_submit()):
        fecha1 = request.form.get("fecha1")
        fecha2 = request.form.get("fecha2")

        #nombre = "nestor"
        #contra = "123"
        #usuario = {'nombre': nombre, 'contra': contra}
        #cookie = requests.post("https://dssdapi.fly.dev/api/log/", usuario)

        reserva = {'fabricante': idfabricante, 'fecha1': fecha1, 'fecha2': fecha2}
        idreserva = requests.post("https://dssdapi.fly.dev/api/reservarf/", reserva)
        EspacioFabricacion.crear(int(idreserva.content), idcoleccion)

        return redirect(url_for("espacioFabricacion_index", idcoleccion = idcoleccion))
    return render_template("espacioFabricacion/new.html", form=form, idcoleccion=idcoleccion, idfabricante=idfabricante) 