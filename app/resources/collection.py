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
from app.models.collection import Collection
from app.models.reservaMateriales import ReservaMateriales
from app.models.espacioFabricacion import EspacioFabricacion
from app.models.planComercial import PlanComercial
import requests
import json

@login_required
def index():
    page =request.args.get('page',1,type=int)
    collections = Collection.query.order_by(Collection.nombre)\
            .paginate(page=page, per_page=5, error_out=False)
    rol= session["rol"]
    aux = []
    for collection in collections.items:
        if PlanComercial.existe(collection.id):
            aux.append({"TienePlan": False,"Id": collection.id})
        else:
            aux.append({"TienePlan": True,"Id": collection.id})
    print(aux)
    return render_template("collection/index.html",collections=collections,rol=rol,aux=aux)

@login_required
def new():
    form = Form_collection_new()
    return render_template("collection/new.html",form=form) 

@login_required
def create():
    form = Form_collection_new()    
    if (form.validate_on_submit()):
        nombre = request.form.get("nombre")
        tipo = request.form.get("tipo")
        plazoF = request.form.get("plazoF")
        fechaL = request.form.get("fechaL")
        adicional = request.form.get("adi")
        cId=Collection.crear(nombre, tipo, plazoF, fechaL)
        cookie = session.get("cookie")
        js = session.get("js")
        aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
        headers = {'Cookie': aux}
        response = requests.get(url="http://localhost:8080/bonita/API/bpm/process/?s=Diseño",headers=headers)
        processid = response.json()[0]["id"]
        headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
        response = requests.post("http://localhost:8080/bonita/API/bpm/process/"+processid+"/instantiation", headers = headers)
        caseid = response.json()["caseId"]
        Collection.setCaseId(cId,caseid)
        caseid=str(caseid)
        response = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+caseid+"",headers=headers)
        taskId = response.json()[0]["id"]
        response = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"4"},headers=headers)
        response = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
        print (response)


        return redirect(url_for("collection_index"))
    return render_template("collection/new.html",form=form) 

@login_required
def detalle(idcoleccion):
    coleccion = Collection.detalle(idcoleccion)
    caseId = coleccion.caseId
    reservas = ReservaMateriales.reservasPorColeccion(idcoleccion)
    cookie = session.get("cookie")
    js = session.get("js")
    aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
    headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}

    #Consulta para ver si se termino todo
    response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Comprobar entrega de materiales",headers=headers).json()
    for instancia in response:
        if int(instancia["caseId"]) == int(caseId) and instancia["displayName"] == "Comprobar entrega de materiales":
            print("Entro en el if")
            if ReservaMateriales.terminaronTodasReservas(idcoleccion):
                response3 = requests.put(url="http://localhost:8080/bonita/API/bpm/caseVariable/"+str(caseId)+"/entregaMateriales",json={"type":"java.lang.Boolean", "value": "true"},headers=headers)
            response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers)
            taskId = response2.json()[0]["id"]
            response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"18"},headers=headers)
            response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
    
    response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Comprobar si se completaron todas las etapas",headers=headers).json()
    for instancia in response:
        if int(instancia["caseId"]) == int(caseId) and instancia["displayName"] == "Comprobar si se completaron todas las etapas":
            print("Entro en el if")
            if EspacioFabricacion.query.filter_by(idcoleccion = idcoleccion).first().estado == "si":
                response3 = requests.put(url="http://localhost:8080/bonita/API/bpm/caseVariable/"+str(caseId)+"/finalizacionEtapasF",json={"type":"java.lang.Boolean", "value": "true"},headers=headers)
                flash("SAAAAAAAAAAAAAPPPPEEEEEEEEEEEE")
            response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers)
            taskId = response2.json()[0]["id"]
            response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"18"},headers=headers)
            response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
    
    
    reservaMateriales = ReservaMateriales.query.filter_by(idcoleccion = idcoleccion).all() #id de todas las reservas para esa coleccion
    i = 0
    aux = [] #Json con todos los materiales
    while i < len(reservaMateriales):
        materiales = requests.get("https://dssdapi.fly.dev/api/listarr/" + str(reservaMateriales[i].idreserva))
        aux.append({"Nombre": materiales.json()["Material"],"Cantidad": materiales.json()["Cantidad"], "Id": materiales.json()["Id"],"Estado": materiales.json()["Estado"], "Estado en BD": reservaMateriales[i].estado})
        i = i + 1
    return render_template("collection/detalle.html",collection = coleccion, reservas=aux, fabricacion = ReservaMateriales.terminaronTodasReservas(idcoleccion)) 

@login_required
def newReasingarfecha(idreserva):
    form = Form_Date_new()
    return render_template("collection/newDate.html",form=form,idreserva=idreserva) 

@login_required
def reasignarFecha(idreserva):
    #//
    form = Form_Date_new()
    if(form.validate_on_submit()):
        fecha = request.form.get("fecha")
        aux={"fecha": fecha}
        requests.post("https://dssdapi.fly.dev/api/cambiarm/"+str(idreserva)+"/",aux)
        idcoleccion = ReservaMateriales.query.filter_by(idreserva=idreserva).first().idcoleccion
        cookie = session.get("cookie")
        js = session.get("js")
        aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
        headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
        caseId=Collection.getCaseid(idcoleccion)
        response3 = requests.put(url="http://localhost:8080/bonita/API/bpm/caseVariable/"+str(caseId)+"/incumplimientoFechas",json={"type":"java.lang.Boolean", "value": "false"},headers=headers)
        response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers)
        taskId = response2.json()[0]["id"]
        response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"18"},headers=headers)
        response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
        return redirect(url_for("collection_index"))
    return render_template("collection/newDate.html",form=form,idreserva=idreserva) 