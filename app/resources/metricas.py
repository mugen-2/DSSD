from concurrent.futures import process
from email import header
from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
from app.forms.collection_form import Form_collection_new
from app.forms.newDate_form import Form_Date_new
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user
from app.models.importacion import Importacion
from app.models.collection import Collection
import requests
import json

@login_required
def index():
    
    return render_template("metricas/index.html")

@login_required
def cantResxMaterial():
    reservas = requests.get("https://dssdapi.fly.dev/api/listarr/").json()["reservas"][0]
    materiales = requests.get("https://dssdapi.fly.dev/api/materiales/").json()["materiales"][0]
    lenght=len(materiales)
    list = [0] * lenght
    for reserva in reservas:
        list[int(reserva["Material"])-1] = list[int(reserva["Material"])-1] + 1
    aux= []
    for material in materiales:
        print(type(material))
        aux.append( { "Nombre":material["Nombre"], "Cantidad":list[material["Id"] - 1] })

    print(aux)
    return render_template("metricas/cantResxMaterial.html",list=aux)

@login_required
def cantImportColeccion():
    importaciones = Importacion.query.all()
    print(len(importaciones))
    return render_template("metricas/cantImportaciones.html",CantI=len(importaciones))

@login_required
def bonita1():
    cookie = session.get("cookie")
    js = session.get("js")
    aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
    headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}

    tareas = requests.get(url="http://localhost:8080/bonita/API/bpm/archivedHumanTask?p=0&f=name=Re-asignar fechas con fabricantes",headers=headers).json()
    CantR= len(tareas)
            
    print(CantR)
    return render_template("metricas/bon1.html",CantR=CantR)