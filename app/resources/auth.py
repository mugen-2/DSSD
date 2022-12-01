from os import environ, urandom
from flask import redirect, render_template, request, url_for, abort, session, flash,current_app
from sqlalchemy.sql.expression import true
from sqlalchemy.util.langhelpers import NoneType
#from app.db import connection
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
import requests, ast

import json
import requests
from oauthlib.oauth2 import WebApplicationClient

def login():
    return render_template("auth/login.html")

# Funcion de autenticacion de sesion y logueo
def authenticate():
    email = request.form.get('email')
    password = request.form.get('password')
    #recordar = request.form.get('recordar')
    user = User.query.filter_by(email=email).first()
    

    if user and check_password_hash(user.password, password):
        session["rol"] = "ADMIN"
        if user.area != "ADMIN":
            passwordB = User.getPasswordB(user.id)
            userB= User.getUserB(user.id)
            session["id"] = user.id
            identification = {'username':userB, 'password': passwordB}
            response = requests.post("http://localhost:8080/bonita/loginservice", identification)
            if(response.status_code == 401):
                flash('Credenciales de la organizacion invalidas')
                return redirect(url_for("auth_login"))
            #print(response)
            session["cookie"] = response.cookies.get_dict()["X-Bonita-API-Token"]
            session["js"] = response.cookies.get_dict()["JSESSIONID"]
            session["JSE"] = "JSESSIONID=" + response.cookies.get("JSESSIONID")
            userBID= getUserBID()
            params = {"f": "user_id=" + userBID, "d": "role_id"}  
            headers = {
                "Cookie": session["JSE"],
                "X-Bonita-API-Token": session["cookie"]
            }
            URL="http://localhost:8080/bonita/API/identity/membership"
            response = requests.Session().get(URL,headers=headers,params=params)
            session["rol"] = response.json()[0]["role_id"]["name"]

        flash('Se ha logueado correctamente') 
        login_user(user)
        return redirect(url_for("home"))
    else:
        flash('credenciales invalidas, intente nuevamente')
        return redirect(url_for("auth_login"))

@login_required
def logout():
    if current_user.area != "ADMIN":
        #session.pop('coockie', None)
        for key in list(session.keys()):
            session.pop(key)
        response = requests.get("http://localhost:8080/bonita/logoutservice")
    logout_user()
    return redirect(url_for("auth_login"))

def getUserBID():
        headers = {
            "Cookie": session["JSE"],
            "X-Bonita-API-Token": session["cookie"]
        }
        response = requests.get("http://localhost:8080/bonita/API/system/session/unusedid",headers=headers) 
        userBId=response.json()["user_id"]
        return userBId