import graphene
from graphene_mongo import MongoengineObjectType
from .models import Miembro as MiembroModel

class Miembro(MongoengineObjectType):
    class Meta:
        model = MiembroModel

# Añade el tipo Miembro a tu Query si aún no lo has hecho
class Query(graphene.ObjectType):
    # ... tus otras definiciones de query
    all_miembros = graphene.List(Miembro)

    def resolve_all_miembros(self, info):
        return list(MiembroModel.objects.all())

# No olvides actualizar tu esquema si es necesario
schema = graphene.Schema(query=Query)