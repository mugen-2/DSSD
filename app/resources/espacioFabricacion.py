from concurrent.futures import process
from email import header
from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
#from app.forms.espacioFabricacion_form import Form_espacioFabricacion_new
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user
#from app.models.espacioFabricacion import EspacioFabricacion
import requests
import json

def index(idcoleccion):
    response = requests.get("https://dssdapi.fly.dev/api/listarf/")
    espaciosFabricacion = response.json()["fabricantes"][0]
    return render_template("espacioFabricacion/index.html",espaciosFabricacion=espaciosFabricacion, idcoleccion=idcoleccion)