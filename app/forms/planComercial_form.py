from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from sqlalchemy.sql.expression import true
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, HiddenField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from wtforms.fields.html5 import EmailField, IntegerField
from app.models.planComercial import PlanComercial


class Form_planComercial_new(FlaskForm):
    
    fechaDeSalida= DateField('fechaDeSalida', 
        validators=[DataRequired( message = "el campo es obligatorio (yyyy-m-d)")])

    lotes= IntegerField('lotes', 
        validators=[DataRequired( message = "el campo es obligatorio")])

class Form_planComercial_verificar(FlaskForm):

    idorden= IntegerField('idorden', 
        validators=[DataRequired( message = "el campo es obligatorio")])