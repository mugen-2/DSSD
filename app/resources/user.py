from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
from app.forms.user_form import Form_usuario_new, Form_usuario_update,Form_usuario_update_p
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user


# Protected resources
#def index():
   #return render_template("home.html")

