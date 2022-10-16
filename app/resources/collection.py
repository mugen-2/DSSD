from concurrent.futures import process
from email import header
from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
from app.forms.collection_form import Form_collection_new
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user
from app.models.collection import Collection
import requests
import json

@login_required
def index():
    page =request.args.get('page',1,type=int)
    collections = Collection.query.order_by(Collection.nombre)\
            .paginate(page=page, per_page=5, error_out=False)
    return render_template("collection/index.html",collections=collections)

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
        Collection.crear(nombre, tipo, plazoF, fechaL)
        cookie = session.get("cookie")
        js = session.get("js")
        aux = "bonita.tenant=1; BOS_Locale=es; JSESSIONID="+js+"; X-Bonita-API-Token="+cookie
        headers = {'Cookie': aux}
        response = requests.get(url="http://localhost:8080/bonita/API/bpm/process/?s=Diseño",headers=headers)
        processid = response.json()[0]["id"]
        headers = {'Cookie': aux, "X-Bonita-API-Token": cookie}
        requests.post("http://localhost:8080/bonita/API/bpm/process/"+processid+"/instantiation", headers = headers)
        return redirect(url_for("collection_index"))
    return render_template("collection/new.html",form=form) 