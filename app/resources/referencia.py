from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.ordenacion import Ordenacion
#from app.db import connection
from app.models.user import User
from app.models.rol import Rol
from app.models.config import Config
#from app.helpers.auth import authenticated
from flask_wtf import FlaskForm
from app.forms.user_form import Form_usuario_new, Form_usuario_update,Form_usuario_update_p
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from app.helpers.auth import authorized
from flask_login import login_required,current_user


# Protected resources
@login_required
def index():
    if authorized("usuario_index"):

        #conn = connection()
        #users = User.all(conn)
        page =request.args.get('page',1,type=int)
        config = Config.query.first()
        ordenacion = Ordenacion.query.filter_by(id = config.ordenacion).first()
    
        users = User.query.order_by(ordenacion.tipo)\
            .paginate(page=page, per_page=config.e_pagina, error_out=False)
        return render_template("user/index.html", users=users)
    else:
        abort(401)

@login_required
def new():
    #if not authenticated(session):
     #   abort(401)
    if authorized("usuario_new"):
        form = Form_usuario_new()
        roles = Rol.query.all()
        rolE = Rol.query.get(50)
        roles.remove(rolE)

        return render_template("user/new.html", form=form,roles=roles)
    else:
        abort(401)

@login_required
def create():
    #if not authenticated(session):
    #    abort(401)
    #conn = connection()
    #User.create(conn, request.form)
    if authorized("usuario_new"):
        id_roles = request.form.getlist("roles")
        form = Form_usuario_new()
        roles = Rol.query.all()
        rolE = Rol.query.get(50)
        roles.remove(rolE)

        form.roles.data = id_roles
        if (form.validate_on_submit()):
            nombre = request.form.get("nombre")
            apellido = request.form.get("apellido")
            email = request.form.get("email")
            password = request.form.get("password")
            username = request.form.get("username")
            id_roles = form.roles.data
            password = generate_password_hash(password)

            User.crear(nombre,apellido,email,password,username,id_roles)
            return redirect(url_for("user_index"))

        return render_template("user/new.html",form=form,roles=roles) 
    else:
        abort(401)

@login_required
def delete(user_id):
   
    if authorized("usuario_destroy"):
        user = User.query.filter_by(id=user_id).first()
        
        if(user):
            if(user.id != current_user.id):
                User.delete(user)
            else: 
                flash("No se puede eliminar a si mismo")
        return redirect(url_for("user_index"))
    else:
        abort(401)


@login_required
def new_update(user_id):
    if authorized("usuario_update"):
        form = Form_usuario_update()
        formp = Form_usuario_update_p()
        user = User.query.filter_by(id=user_id).first()
        return render_template("user/update.html", form=form, formp=formp, user = user)
    else:
        abort(401)

@login_required
def update(user_id):
    
    if authorized("usuario_update"):
        form = Form_usuario_update()
        formp = Form_usuario_update_p()
        user = User.query.filter_by(id=user_id).first()
        if(user):
            if (form.validate_on_submit()):
                nombre = request.form.get("nombre")
                apellido = request.form.get("apellido")
                email = request.form.get("email")
                password = request.form.get("password")
                username = request.form.get("username")

                User.editar(user_id,nombre,apellido,email,username)
                return redirect(url_for("user_index"))
        
            if (formp.validate_on_submit()):
                password_n = request.form.get("password_n")
                password_n = generate_password_hash(password_n)
            
                User.editar_p(user_id,password_n)
                return redirect(url_for("user_index"))
        
 
        return render_template("user/update.html",user = user,form=form,formp=formp)
    else:
        abort(401)

@login_required
def new_assign_rol(user_id):
    if authorized("usuario_asignar_rol"):
        roles = Rol.query.all()
        rolE = Rol.query.get(50)
        roles.remove(rolE)

        user = User.query.filter_by(id=user_id).first()
        userR=user.roles
        userR.remove(rolE)
        for rolu in user.roles:
            roles.remove(rolu)
        return render_template("user/assign_rol.html",roles=roles,user=user )
    else:
        abort(401)

@login_required
def assign_rol(user_id,rol_id):
    #user = User.query.filter_by(id=user_id).first()
    #roles = Rol.query.all()
    User.assign_rol(user_id,rol_id)     
    return redirect(url_for("user_index"))

@login_required
def unassign_rol(user_id,rol_id):
    #user = User.query.filter_by(id=user_id).first()
    #roles = Rol.query.all()
    User.unassign_rol(user_id,rol_id)
    return redirect(url_for("user_index"))
    
@login_required
def block (user_id):
    if authorized("usuario_block"):
        user = User.query.filter_by(id=user_id).first()

        if(user):
            User.block(user_id)
        return redirect(url_for("user_index"))

    else:
        abort(401)
    
@login_required    
def search():

    if authorized("usuario_index"):

        page =request.args.get('page',1,type=int)
        config = Config.query.first()
        ordenacion = Ordenacion.query.filter_by(id = config.ordenacion).first()
        if request.form.get("estado") == None:
            estado = 0
        else:
            estado = 1

        usernamep = request.form.get("username")
        search = "%{}%".format(usernamep)
        busco=1

        users = User.query.filter(db.and_(User.username.like(search), User.activo==estado))\
            .order_by(ordenacion.tipo)\
            .paginate(page=page, per_page=config.e_pagina, error_out=False)
        
    # users = User.query.filter_by(username = usernamep)\
        #    .order_by(ordenacion.tipo)\
        #   .paginate(page=page, per_page=config.e_pagina, error_out=False)
        return render_template("user/index.html", users=users,busco=busco)
    else:
        abort(401)

@login_required
def confirmarUsuarios():
    if authorized("usuario_confirm"):


        page =request.args.get('page',1,type=int)
        config = Config.query.first()
        ordenacion = Ordenacion.query.filter_by(id = config.ordenacion).first()

        roles = Rol.query.all()
     
        rolE = Rol.query.get(50)
     
        roles.remove(rolE)

        users= User.query.filter_by(confirmados= 0) \
            .order_by(ordenacion.tipo)\
            .paginate(page=page, per_page=config.e_pagina, error_out=False)
        return render_template("user/confirm.html", users=users, roles=roles)
    else:
        abort(401)

@login_required
def confirmar (user_id):
    if authorized("usuario_confirm"):
        user = User.query.get(user_id)

        if(user):
            User.confirmU(user_id)
        return redirect(url_for("new_user_assign_rol",user_id=user.id))

    else:
        abort(401)


