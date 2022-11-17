from concurrent.futures import process
from email import header
from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
from app.forms.reservaMateriales_form import Form_reservaMateriales_new
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user
from app.models.reservaMateriales import ReservaMateriales
import requests
import json

def index(idcoleccion):
    page =request.args.get('page',1,type=int)
    reservaMateriales = ReservaMateriales.query.filter_by(idcoleccion = idcoleccion)\
            .paginate(page=page, per_page=5, error_out=False) #id de todas las reservas para esa coleccion
    
    #i = 0
    #reservaMateriales = []
    #while i < len(idReservas):
        #materiales = requests.get("https://dssdapi.fly.dev/api/materiales/" + idReservas[i].reservas)
        #print (materiales.json)
        #print(materiales.content)
        #reservaMateriales.append({"Nombre": materiales.nombre,"Cantidad": materiales.cantidad})
        #i = i + 1
    
    return render_template("reservaMateriales/index.html", reservaMateriales=reservaMateriales, idcoleccion=idcoleccion)

def list(idcoleccion):
    response = requests.get("https://dssdapi.fly.dev/api/materiales/")
    materiales = response.json()["materiales"][0]
    return render_template("reservaMateriales/list.html",materiales=materiales, idcoleccion=idcoleccion) 

def new(idcoleccion, idmaterial):
    form = Form_reservaMateriales_new()
    return render_template("reservaMateriales/new.html", form=form, idcoleccion=idcoleccion, idmaterial=idmaterial) 

def create(idcoleccion, idmaterial):
    form = Form_reservaMateriales_new()    
    if (form.validate_on_submit()):
        fechaE = request.form.get("FechaEntrega")
        cantidad = request.form.get("cantidad")
        cantidad = int(cantidad)

        nombre = "nestor"
        contra = "123"
        usuario = {'nombre': nombre, 'contra': contra}
        cookie = requests.post("https://dssdapi.fly.dev/api/log/", usuario)

        reserva = {'id': idmaterial, 'cantidad': cantidad, 'fecha': fechaE, 'cookie': cookie.content}
        idreserva = requests.post("https://dssdapi.fly.dev/api/reserva/", reserva)
        ReservaMateriales.crear(int(idreserva.content), idcoleccion)

        return redirect(url_for("reservaMateriales_index", idcoleccion = idcoleccion))
    return render_template("reservaMateriales/new.html", form=form, idcoleccion=idcoleccion, idmaterial=idmaterial)     

