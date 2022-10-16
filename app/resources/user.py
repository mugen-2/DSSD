from flask import redirect, render_template, request, url_for, session, abort, flash
#from app.db import connection
from app.models.user import User
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
from app.forms.user_form import Form_usuario_new
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user


# Protected resources
@login_required
def index():
   page =request.args.get('page',1,type=int)
   users = User.query.order_by(User.first_name)\
      .paginate(page=page, per_page=5, error_out=False)
   return render_template("user/index.html", users=users)

@login_required
def new():
   form = Form_usuario_new()
   return render_template("user/new.html", form=form)

@login_required
def create():
   form = Form_usuario_new()
   if (form.validate_on_submit()):
      nombre = request.form.get("nombre")
      apellido = request.form.get("apellido")
      email = request.form.get("email")
      password = request.form.get("password")
      username = request.form.get("username")
      areas= request.form.get("areas")
      password = generate_password_hash(password)
      usernameB = request.form.get("usernameB")
      passwordB = request.form.get("passwordB")


      User.crear(nombre,apellido,email,password,username,areas,usernameB,passwordB)
      return redirect(url_for("user_index"))

   return render_template("user/new.html",form=form) 

@login_required
def delete(user_id):
   user = User.query.filter_by(id=user_id).first()
   if(user):
      if(user.id != current_user.id):
            User.delete(user)
      else: 
            flash("No se puede eliminar a si mismo")
   return redirect(url_for("user_index"))