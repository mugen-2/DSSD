from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from sqlalchemy.sql.expression import true
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from wtforms.fields.html5 import EmailField, IntegerField
from app.models.user import User

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

    areas = SelectField('areas',
        choices=[('1','Diseñador'), ('2','Operador'), ('3','Comercial')],
        validators=[DataRequired( message ="el campo es obligatorio")])
    
    usernameB = StringField('usernameB',
        validators=[DataRequired( message = "el campo es obligatorio")])

    passwordB = PasswordField ('passwordB',
        validators=[DataRequired( message = "el campo es obligatorio"),
        Length(min = 6, message=("la contraseña tiene que tener como minimo 6 caracteres"))])

    def validate_email(form, email):
        if ((User.query.filter_by(email=email.data).first()) != None):
            raise ValidationError("el email no esta disponible")

    def validate_username (form, username):
        if ((User.query.filter_by(username=username.data).first()) != None):
            raise ValidationError("el nombre de usuario no esta disponible")

