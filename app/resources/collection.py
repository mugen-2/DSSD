from concurrent.futures import process
from email import header
from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
from app.forms.collection_form import Form_collection_new
from app.forms.newDate_form import Form_Date_new
from app.forms.Importacion_form import Form_Importacion_new
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user
from app.models.collection import Collection
from app.models.reservaMateriales import ReservaMateriales
from app.models.espacioFabricacion import EspacioFabricacion
from app.models.planComercial import PlanComercial
from app.models.importacion import Importacion
import requests
import json

@login_required
def index():
    page =request.args.get('page',1,type=int)
    collections = Collection.query.order_by(Collection.nombre)\
            .paginate(page=page, per_page=5, error_out=False)
    rol= session["rol"]
    x = []
    cookie = session.get("cookie")
    js = session.get("js")
    aux= "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
    headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
    response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Asociar lotes con ordenes",headers=headers).json()
    for istancia in response:
        if istancia["displayName"] == "Asociar lotes con ordenes":
            x.append({"CaseId": istancia["caseId"]})
    aux = []
    for collection in collections.items:
        aux2 = False
        if PlanComercial.existe(collection.id):
            aux.append({"TienePlan": False,"Id": collection.id, "AsignarLotes": aux2})
        else:
            for y in x:
                if int(y["CaseId"]) == int(collection.caseId):
                    aux2 = True
            aux.append({"TienePlan": True,"Id": collection.id, "AsignarLotes": aux2})
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
            response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers).json()
            for x in response2:
                if x["displayName"] == "Comprobar entrega de materiales":
                    taskId = x["id"]
            response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"18"},headers=headers)
            response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
    #Consulta para ver si se terminaron todas las etapas de fabricacion
    response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Comprobar si se completaron todas las etapas",headers=headers).json()
    for instancia in response:
        if int(instancia["caseId"]) == int(caseId) and instancia["displayName"] == "Comprobar si se completaron todas las etapas":
            print("Entro en el if")
            if EspacioFabricacion.query.filter_by(idcoleccion = idcoleccion).first().estado == "si":
                response3 = requests.put(url="http://localhost:8080/bonita/API/bpm/caseVariable/"+str(caseId)+"/finalizacionEtapasF",json={"type":"java.lang.Boolean", "value": "true"},headers=headers)
                #flash("SAAAAAAAAAAAAAPPPPEEEEEEEEEEEE")
            response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers).json()
            for x in response2:
                if x["displayName"] == "Comprobar si se completaron todas las etapas":
                    taskId = x["id"]
            response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"18"},headers=headers)
            response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
    
    reservaMateriales = ReservaMateriales.query.filter_by(idcoleccion = idcoleccion).all() #id de todas las reservas para esa coleccion
    i = 0
    aux = [] #Json con todos los materiales
    while i < len(reservaMateriales):
        materiales = requests.get("https://dssdapi.fly.dev/api/listarr/" + str(reservaMateriales[i].idreserva))
        aux.append({"Nombre": materiales.json()["Material"],"Cantidad": materiales.json()["Cantidad"], "Id": materiales.json()["Id"],"Estado": materiales.json()["Estado"], "Estado en BD": reservaMateriales[i].estado})
        i = i + 1

    reasignar = False
    response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Re-asignar fechas con fabricantes",headers=headers).json()
    for instancia in response:
        if int(instancia["caseId"]) == int(caseId) and instancia["displayName"] == "Re-asignar fechas con fabricantes":
            reasignar = True
    print(reasignar)
    print(aux)
    return render_template("collection/detalle.html",collection = coleccion, reservas=aux, fabricacion = ReservaMateriales.terminaronTodasReservas(idcoleccion), reasignar=reasignar) 

@login_required
def newReasingarfecha(idreserva):
    form = Form_Date_new()
    return render_template("collection/newDate.html",form=form,idreserva=idreserva) 

@login_required
def reasignarFecha(idreserva):
    #//
    form = Form_Date_new()
    if(form.validate_on_submit()):
        reserva = ReservaMateriales.query.filter_by(idreserva=idreserva).first()
        idFabricacion = EspacioFabricacion.query.filter_by(idcoleccion=reserva.idcoleccion).first().idreserva
        print(idFabricacion)

        fecha = request.form.get("fecha")
        fecha2 = request.form.get("fecha2")
        aux = {"fecha1": fecha, "fecha2": fecha2}
        idreserva1 = requests.post("https://dssdapi.fly.dev/api/cambiarf/"+str(idFabricacion)+"/",aux).json()
        if idreserva1["ReservaFabricacion"] != "No se puede reservar para dicho peirodo de tiempo":
            aux = {"id":idreserva}
            requests.post("https://dssdapi.fly.dev/api/riniciar/",aux)
            idcoleccion = ReservaMateriales.query.filter_by(idreserva=idreserva).first().idcoleccion
            cookie = session.get("cookie")
            js = session.get("js")
            aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
            headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
            caseId=Collection.getCaseid(idcoleccion)
            response3 = requests.put(url="http://localhost:8080/bonita/API/bpm/caseVariable/"+str(caseId)+"/incumplimientoFechas",json={"type":"java.lang.Boolean", "value": "false"},headers=headers)
            response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers).json()
            for x in response2:
                if x["displayName"] == "Re-asignar fechas con fabricantes":
                    taskId = x["id"]
            response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"18"},headers=headers)
            response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
            return redirect(url_for("collection_index"))
        else:
            flash("No se puede reservar en ese periodo de fechas")
    return render_template("collection/newDate.html",form=form,idreserva=idreserva) 

@login_required
def newImportacion(idcoleccion):
    form = Form_Importacion_new()
    return render_template("collection/newImportacion.html",form=form,idcoleccion=idcoleccion)

@login_required
def importacion(idcoleccion):
    form = Form_Importacion_new()
    if(form.validate_on_submit()):
        codigop = request.form.get("codigop")
        direccion = request.form.get("direccion")
        Importacion.crear(codigop,direccion,idcoleccion)
        cookie = session.get("cookie")
        js = session.get("js")
        aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
        headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
        caseId = Collection.getCaseid(idcoleccion)
        response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers).json()
        for x in response2:
                if x["displayName"] == "importar materiales":
                    taskId = x["id"]
        response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"18"},headers=headers)
        response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
        return redirect(url_for("collection_index"))
    return render_template("collection/newImportacion.html",form=form,idcoleccion=idcoleccion) 