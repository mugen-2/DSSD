from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from sqlalchemy.sql.expression import true
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from wtforms.fields.html5 import EmailField, IntegerField
from app.models.user import User
from app.models.rol import Rol

from sqlalchemy import and_, Column
from werkzeug.security import generate_password_hash, check_password_hash


class Form_usuario_new(FlaskForm):
    
    nombre = StringField('nombre', 
        validators=[DataRequired( message = "el campo es obligatorio")])

    apellido = StringField('apellido',
        validators=[DataRequired( message = "el campo es obligatorio")])

    email = EmailField('email',
        validators=[DataRequired( message = "el campo es obligatorio"),
        Email(message="no cumple el formato de mail")])

    username = StringField('username',
        validators=[DataRequired( message = "el campo es obligatorio")])

    password = PasswordField ('password',
        validators=[DataRequired( message = "el campo es obligatorio"),
        Length(min = 6, message=("la contraseña tiene que tener como minimo 6 caracteres"))])

    roles = SelectMultipleField('roles',
        choices=[('1','Administrador'), ('2','Operador')],
        validators=[DataRequired( message ="el campo es obligatorio")])
    
    def validate_email(form, email):
        if ((User.query.filter_by(email=email.data).first()) != None):
            raise ValidationError("el email no esta disponible")

    def validate_username (form, username):
        if ((User.query.filter_by(username=username.data).first()) != None):
            raise ValidationError("el nombre de usuario no esta disponible")

class Form_usuario_update(FlaskForm):
    
    nombre = StringField('nombre', validators=[DataRequired( message = "el campo es obligatorio")])

    apellido = StringField('apellido', validators=[DataRequired( message = "el campo es obligatorio")])

    email = EmailField('email', validators=[DataRequired( message = "el campo es obligatorio"),Email(message="no cumple el formato de mail")])

    username = StringField('username', validators=[DataRequired( message = "el campo es obligatorio")])

    id = IntegerField('id')

    def validate_email(form, email):
        persona = User.query.filter_by(email=email.data).first()
        if persona != None and persona.id != form.id.data:
            raise ValidationError("el mail ya esta en uso")

    def validate_username (form, username):
        persona = User.query.filter_by(username=username.data).first()
        if persona != None and persona.id != form.id.data:
            raise ValidationError("el nombre de usuario no esta disponible")

class Form_usuario_update_p(FlaskForm):
    
    password_o = PasswordField ('password_o', validators=[DataRequired( message = "el campo es obligatorio"),Length(min = 6, message=("la contraseña tiene que tener como minimo 6 caracteres"))])
    password_n = PasswordField ('password_n', validators=[EqualTo('password_c', message='la contraseña nueva y la confirmacion deben ser iguales'),DataRequired( message = "el campo es obligatorio"),Length(min = 6, message=("la contraseña tiene que tener como minimo 6 caracteres"))])
    password_c = PasswordField ('password_c', validators=[DataRequired( message = "el campo es obligatorio"),Length(min = 6, message=("la contraseña tiene que tener como minimo 6 caracteres"))])

    idp = IntegerField('idp')

    def validate_password_o(form, password_n):
        print (form.password_n.data)
        print (form.password_o.data)
        print (form.password_c.data)
        persona = User.query.filter_by(id=form.idp.data).first()
        if check_password_hash(persona.password,form.password_o.data):
            if check_password_hash(persona.password,form.password_n.data):
                raise ValidationError("La contraseña nueva debe ser distinta a la anterior")
        else:
            raise ValidationError("No esta ingresando la contraseña antigua de forma correcta")
