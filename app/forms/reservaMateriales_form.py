from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from sqlalchemy.sql.expression import true
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, HiddenField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from wtforms.fields.html5 import EmailField, IntegerField
from app.models.reservaMateriales import ReservaMateriales


class Form_reservaMateriales_new(FlaskForm):


    nombre= StringField('nombre', 
        validators=[DataRequired( message = "el campo es obligatorio")])

    cantidad= IntegerField('cantidad', 
        validators=[DataRequired( message = "el campo es obligatorio")])
    
    