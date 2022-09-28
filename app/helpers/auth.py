from sqlalchemy.sql.expression import false, true
from app.models.user import User
from flask_login import current_user

def authenticated(session):
    return session.get("user")

def authorized(p):
    ok = False
    permisos_usuario = User.permisos(current_user.id)
    for permiso in permisos_usuario:
        if permiso == p:
            ok = True
    return ok
