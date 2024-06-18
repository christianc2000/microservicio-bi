# flask_graphene_mongo/models.py
from datetime import datetime
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, ReferenceField, StringField,
)


class Evento(Document):
    meta = {'collection': 'eventos'}
    nombre = StringField(required=True)
    fecha = DateTimeField(required=True)  # Changed from StringField to DateTimeField
    lugar = StringField(required=True)
    
    @staticmethod
    def obtener_recaudacion_eventos():
        pipeline = [
            {"$group": {
                "_id": "$eventoId",
                "total_recaudado": {"$sum": {"$toDouble": "$monto"}}
            }}
        ]
        recaudaciones = Donacion.objects.aggregate(*pipeline)
        return recaudaciones

class Miembro(Document):
    meta = {'collection': 'miembros',
            'allow_inheritance': False}
    ci= StringField(required=True)
    nombre= StringField(required=True)
    apellido= StringField(required=True)
    foto= StringField(required=True)
    fechaNacimiento= StringField(required=True)
    celular= StringField(required=True)
    genero= StringField(required=True)


class Asistencia(Document):
    meta = {'collection': 'asistencias',
            'allow_inheritance': False}
    fecha= StringField(required=True)
    eventoId= StringField(required=True)
    miembroId= StringField(required=True)

class TipoDonacion(Document):
    meta = {'collection': 'tipo_donacions',
            'allow_inheritance': False}
    nombre= StringField(required=True)

class Donacion(Document):
    meta = {'collection': 'donacions',
            'allow_inheritance': False}
    monto= StringField(required=True)
    fecha= DateTimeField(required=True)
    miembroId= StringField(required=True)
    eventoId= StringField(required=True)
    tipoDonacionId= StringField(required=True)
