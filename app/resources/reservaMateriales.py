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
            .paginate(page=page, per_page=5, error_out=False)
    return render_template("reservaMateriales/index.html", reservaMateriales=reservaMateriales, idcoleccion=idcoleccion)

def list(idcoleccion):
    response = requests.get("https://dssdapi.fly.dev/api/materiales/")
    materiales = response.json()["materiales"][0]
    return render_template("reservaMateriales/list.html",materiales=materiales, idcoleccion=idcoleccion) 

def new(idcoleccion):
    form = Form_reservaMateriales_new()
    return render_template("reservaMateriales/new.html", form=form, idcoleccion=idcoleccion) 

def create(idcoleccion):
    form = Form_reservaMateriales_new()    
    if (form.validate_on_submit()):
        fechaE = request.form.get("FechaEntrega")
        cantidad = request.form.get("cantidad")

        
        #ReservaMateriales.crear(fechaE, cantidad, idcoleccion)
        cookie = session.get("cookie")
        js = session.get("js")
        aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
        headers = {'Cookie': aux}
        response = requests.get(url="http://localhost:8080/bonita/API/bpm/process/?s=Diseño",headers=headers)
        processid = response.json()[0]["id"]
        headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
        requests.post("http://localhost:8080/bonita/API/bpm/process/"+processid+"/instantiation", headers = headers)
        return redirect(url_for("reservaMateriales_index", idcoleccion = idcoleccion))
    return render_template("reservaMateriales/new.html",form=form) 

