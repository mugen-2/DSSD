from concurrent.futures import process
from email import header
from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from app.models.collection import Collection
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
    cookie = session.get("cookie")
    js = session.get("js")
    aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
    headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
    response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Reserva de materiales",headers=headers).json()  # Buscamos para poder avanzar la tarea
    caseId = Collection.getCaseid(idcoleccion)
    for instancia in response:
        if int(instancia["caseId"]) == int(caseId) and instancia["displayName"] == "Reserva de materiales":
            response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers)
            taskId = response2.json()[0]["id"]
            response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"18"},headers=headers)
            response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)

    response = requests.get("https://dssdapi.fly.dev/api/listarf/")
    espaciosFabricacion = response.json()["fabricantes"][0]
    espacio = EspacioFabricacion.tieneEspacioFabricacion(idcoleccion)
    notiene=True
    if espacio:
        notiene = False
    return render_template("espacioFabricacion/index.html",espaciosFabricacion=espaciosFabricacion, idcoleccion=idcoleccion, notiene=notiene)

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

        reserva= {'fabricante': idfabricante, 'fecha1': fecha1, 'fecha2': fecha2}
        print(reserva)
        idreserva = requests.post("https://dssdapi.fly.dev/api/reservarf/", reserva).json()
        if idreserva["ReservaFabricacion"] != "No se puede reservar para dicho peirodo de tiempo":
            EspacioFabricacion.crear(int(idreserva["ReservaFabricacion"]), idcoleccion)

            cookie = session.get("cookie")
            js = session.get("js")
            aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
            headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
            response = requests.get(url="http://localhost:8080/bonita/API/bpm/task/?s=Reserva de espacio de fabricacion",headers=headers).json()
            caseId = Collection.getCaseid(idcoleccion)
            for instancia in response:
                if int(instancia["caseId"]) == int(caseId) and instancia["displayName"] == "Reserva de espacio de fabricacion":
                    response = requests.get(url="https://dssdapi.fly.dev/api/listarf/"+str(idfabricante)+"/").json()
                    if(response["Codigo"]!=54): #Falta poder chequear el codigo de un fabricante en particular
                        response = requests.put(url="http://localhost:8080/bonita/API/bpm/caseVariable/"+str(caseId)+"/hayQueImportar",json={"type":"java.lang.Boolean", "value": "true"},headers=headers)
                        print(response)
                    response2 = requests.get(url="http://localhost:8080/bonita/API/bpm/humanTask?c=10&p=0&f=caseId%3D"+str(caseId)+"",headers=headers)
                    taskId = response2.json()[0]["id"]
                    response2 = requests.put(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"",json={"assigned_id":"18"},headers=headers)
                    response2 = requests.post(url="http://localhost:8080/bonita/API/bpm/userTask/"+taskId+"/execution",headers=headers)
                    if(response["Codigo"]!=54):
                        return redirect(url_for("espacioFabricacion_index", idcoleccion = idcoleccion)) #Hacer un formulario para la importacion en la etapa de fabricacion
            print(caseId)

            return redirect(url_for("collection_index", idcoleccion = idcoleccion))
        else:
            print("Imposible maestro")
    return render_template("espacioFabricacion/new.html", form=form, idcoleccion=idcoleccion, idfabricante=idfabricante) 