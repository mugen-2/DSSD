from concurrent.futures import process
from email import header
from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
from app.forms.planComercial_form import Form_planComercial_new, Form_planComercial_verificar
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user
from app.models.planComercial import PlanComercial
from app.models.ordenCompra import OrdenCompra
from app.models.collection import Collection
from app.models.espacioFabricacion import EspacioFabricacion
from app.resources.auth import getUserBID
import requests
import json
import random

def new(idcoleccion):
    form = Form_planComercial_new()
    return render_template("planComercial/new.html", form=form, idcoleccion=idcoleccion) 

def verificarLotes(idcoleccion):
    caseId = Collection.getCaseid(idcoleccion)
    cookie = session.get("cookie")
    js = session.get("js")
    aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
    headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
    response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Comprobar si se recibieron todos los lotes",headers=headers).json()
    for instancia in response:
            if int(instancia["caseId"]) == int(caseId) and instancia["displayName"] == "Comprobar si se recibieron todos los lotes":
                reservaF = EspacioFabricacion.query.filter_by(idcoleccion = idcoleccion).first()
                if reservaF and reservaF.estado == "si":
                    aleatorio = random.randint(1, 3)
                    print(aleatorio)
                    if aleatorio == 2:
                        flash("Ya llegaron los lotes")
                        response3 = requests.put(url="http://localhost:8080/bonita/API/bpm/caseVariable/"+str(caseId)+"/lotes",json={"type":"java.lang.Boolean", "value": "true"},headers=headers)
                    else:
                        flash("Todavia no llegaron los lotes")
                else:
                    flash("Todavia no se termino de fabricar")
                response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers).json()
                for x in response2:
                    if x["displayName"] == "Comprobar si se recibieron todos los lotes":
                        taskId = x["id"]
                response3 = requests.get("http://localhost:8080/bonita/API/system/session/unusedid",headers=headers) 
                userBId = response3.json()["user_id"]
                response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":userBId},headers=headers)
                response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
    return redirect(url_for("collection_index"))

def create(idcoleccion):
    form = Form_planComercial_new()    
    if (form.validate_on_submit()):
        caseId = Collection.getCaseid(idcoleccion)
        cookie = session.get("cookie")
        js = session.get("js")
        aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
        headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
        response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Dise??ar plan comercial",headers=headers).json()
        for instancia in response:
            if int(instancia["caseId"]) == int(caseId) and instancia["displayName"] == "Dise??ar plan comercial":
                response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers).json()
                for x in response2:
                    if x["displayName"] == "Dise??ar plan comercial":
                        taskId = x["id"]
                response3 = requests.get("http://localhost:8080/bonita/API/system/session/unusedid",headers=headers) 
                userBId = response3.json()["user_id"]
                response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":userBId},headers=headers)
                response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
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

def verificar(idcoleccion):
    form = Form_planComercial_verificar()
    return render_template("planComercial/verificar.html", form=form, idcoleccion=idcoleccion)


def verificar2(idcoleccion):
    form = Form_planComercial_verificar()   
    if (form.validate_on_submit()):
        idorden = request.form.get("idorden")
        idorden = str(idorden)
        ok = OrdenCompra.query.filter_by(orden=idorden).first()
        aux = PlanComercial.query.filter_by(idcoleccion=idcoleccion).first()
        if ok and ok.idplancomercial == aux.id:
            OrdenCompra.actualizar(idorden)
            flash("Se ha verificado el numero de orden")
            if PlanComercial.ordenesDeComprasListas(idcoleccion):
                caseId = Collection.getCaseid(idcoleccion)
                cookie = session.get("cookie")
                js = session.get("js")
                aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
                headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
                response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Asociar lotes con ordenes",headers=headers).json()
                for instancia in response:
                    if int(instancia["caseId"]) == int(caseId) and instancia["displayName"] == "Asociar lotes con ordenes":
                        response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers).json()
                        for x in response2:
                            if x["displayName"] == "Asociar lotes con ordenes":
                                taskId = x["id"]
                        response3 = requests.get("http://localhost:8080/bonita/API/system/session/unusedid",headers=headers) 
                        userBId = response3.json()["user_id"]
                        response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":userBId},headers=headers)
                        response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
                        flash("Todo el proceso ha sido terminado")
            return redirect(url_for("collection_index"))
        else:
            flash("Numero de orden incorrecto")    
    return render_template("planComercial/verificar.html", form=form, idcoleccion=idcoleccion)