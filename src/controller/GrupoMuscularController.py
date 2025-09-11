import re

from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError
from src.service.GrupoMuscularService import addGrupoMuscular,getGruposMusculares,getGrupoMuscular,updateGrupoMuscular,deleteGrupoMuscular

class GrupoMuscularResponseSchema(Schema):
    id=fields.Int()
    nome = fields.Str()

class GrupoMuscularRequestSchema(Schema):
    id=fields.Int()
    nome = fields.Str()

    @validates("nome")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_\s]+$", string=value):
            raise ValidationError("Nome nao pode ser um caracter especial")
        
    
class GrupoMuscularItem(MethodResource,Resource):
    @marshal_with(GrupoMuscularResponseSchema)
    def get(self,grupo_muscular_id):
        try:
            grupoMuscular = getGrupoMuscular(grupo_muscular_id)
            if not grupoMuscular:
                abort(404, message="Resource not found")
            return grupoMuscular, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    def delete(self, grupo_muscular_id):
        try:
            deleteGrupoMuscular(grupo_muscular_id)
            return "", 204
        except UnmappedInstanceError:
            abort(404, message="Resource not found")
        except (OperationalError, IntegrityError):
            abort(500, message="Internal Server Error") 

    @use_kwargs(GrupoMuscularRequestSchema, location=("form"))
    @marshal_with(GrupoMuscularResponseSchema)
    def put(self, grupo_muscular_id, **kwargs):
        try:
            grupoMuscular = updateGrupoMuscular(**kwargs, id=grupo_muscular_id)
            return grupoMuscular, 200
        except (OperationalError, IntegrityError):
           abort(500, message="Internal Server Error")

class GrupoMuscularList(MethodResource, Resource):
    @marshal_with(GrupoMuscularResponseSchema(many=True))
    def get(self):
        try:
            return getGruposMusculares(),200
        except OperationalError:
            abort(500, message="Internal Server Error")
    
    @use_kwargs(GrupoMuscularRequestSchema, location=("form"))
    @marshal_with(GrupoMuscularResponseSchema)
    def post(self, **kwargs):
        try:
            grupoMuscular = addGrupoMuscular(**kwargs)
            return grupoMuscular, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))

 