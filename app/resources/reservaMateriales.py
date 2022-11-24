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
from app.models.collection import Collection
import requests
import json

def index(idcoleccion):
    cookie = session.get("cookie")
    js = session.get("js")
    aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
    headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
    response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Establecer materiales y fechas",headers=headers).json()
    print(response)
    caseId = Collection.getCaseid(idcoleccion)
    print(caseId)
    print("--------------------------------------------------------")
    for instancia in response:
        print(instancia["caseId"])
        if int(instancia["caseId"]) == int(caseId):
            response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers)
            print("--------------------------------------------------------")
            print (response2)
            taskId = response2.json()[0]["id"]
            print(taskId)
            response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"18"},headers=headers)
            print("--------------------------------------------------------")
            print (response2)
            response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)

    page =request.args.get('page',1,type=int)
    reservaMateriales = ReservaMateriales.query.filter_by(idcoleccion = idcoleccion).all() #id de todas las reservas para esa coleccion
    i = 0
    aux = []
    while i < len(reservaMateriales):
        materiales = requests.get("https://dssdapi.fly.dev/api/listarr/" + str(reservaMateriales[i].idreserva))
        aux.append({"Nombre": materiales.json()["Material"],"Cantidad": materiales.json()["Cantidad"]})
        i = i + 1
    
    return render_template("reservaMateriales/index.html", reservaMateriales=aux, idcoleccion=idcoleccion)

def list(idcoleccion):
    cookie = session.get("cookie")
    js = session.get("js")
    aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
    headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
    response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Reserva de materiales",headers=headers).json()    # Buscamos para mostrar o no un boton
    reservar = False
    caseId = Collection.getCaseid(idcoleccion)
    print(caseId)
    for instancia in response:
        print(caseId)
        print(instancia) 
        if int(instancia["caseId"]) == int(caseId) and instancia["displayName"] == "Reserva de materiales":
            reservar = True
    print(reservar)
    response = requests.get("https://dssdapi.fly.dev/api/materiales/")
    materiales = response.json()["materiales"][0]
    return render_template("reservaMateriales/list.html",materiales=materiales, idcoleccion=idcoleccion, reservar = reservar) 

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

