from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from sqlalchemy.sql.expression import true
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, HiddenField, DateField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from wtforms.fields.html5 import EmailField, IntegerField
from app.models.collection import Collection


class Form_collection_new(FlaskForm):

    tipo= StringField('tipo', 
        validators=[DataRequired( message = "el campo es obligatorio")])

    nombre= StringField('nombre', 
        validators=[DataRequired( message = "el campo es obligatorio")])

    plazoF= IntegerField('plazoF', 
        validators=[DataRequired( message = "el campo es obligatorio")])
    
    fechaL= DateField('fechaL', 
        validators=[DataRequired( message = "el campo es obligatorio")])
    
    def validate_nombre(form, nombre):
        if ((Collection.query.filter_by(nombre=nombre.data).first()) != None):
            raise ValidationError("el nombre de coleccion no esta disponible")