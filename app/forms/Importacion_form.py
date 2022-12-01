from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from sqlalchemy.sql.expression import true
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, HiddenField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Email
from wtforms.fields.html5 import EmailField, IntegerField
from app.models.espacioFabricacion import EspacioFabricacion


class Form_Importacion_new(FlaskForm):

    codigop = StringField('codigop',
        validators=[DataRequired( message = "el campo es obligatorio")])

    direccion = StringField('direccion',
        validators=[DataRequired( message = "el campo es obligatorio")])
    