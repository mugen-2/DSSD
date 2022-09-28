from marshmallow import Schema, fields, validate, ValidationError
from marshmallow import fields


class DenunciaSchema(Schema):
    titulo = fields.Str(validate=validate.Length(min=1, error="El titulo no puede ser vacio"), required=True, error_messages={
          'required': {"mensaje": 'El titulo es obligatorio.'}})
    categoria = fields.Str(validate=validate.Length(min=1, error="El titulo no puede ser vacio"), required=True, error_messages={
          'required': "La categoria es obligatoria"})
    descripcion = fields.Str(validate=validate.Length(min=1, error="La descripcion no puede ser vacia"), required=True, error_messages={
          'required': "La descripcion es obligatoria"})
    nombre = fields.Str(validate=validate.Length(min=1, error="El nombre no puede ser vacio"), required=True, error_messages={
          'required': "El nombre es obligatorio"})
    apellido = fields.Str(validate=validate.Length(min=1, error="El apellido no puede ser vacio"), required=True, error_messages={
          'required': "El apellido es obligatorio"})
    telefono = fields.Int(validate=[
        
        validate.Range(min=0, max=99999999999999, error="El telefono no puede ser vacio")
    ], required=True, error_messages={
          'required': "El telefono es obligatorio",
          "invalid": "El telefono solo puede contener numeros"})
    email = fields.Email(validate=validate.Length(min=1, error="El email no puede ser vacio"),required=True, error_messages={
          'required': "El email es obligatorio",
          "invalid": "Debe ser una direccion de email valida"})
    latitud = fields.Float(required=True, error_messages={
          'required': "La latitud es obligatoria",
          "invalid": "Debe ser una latitud valida"})
    longitud = fields.Float(required=True, error_messages={
          'required': "La longitud es obligatoria",
          "invalid": "Debe ser una longitud valida"})

    #default_error_messages["required"] = "My custom required message"