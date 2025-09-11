import re

from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError
from src.service.ExercicioService import addExercicio,getExercicios,getExercicio,updateExercicio,deleteExercicio

class ExercicioResponseSchema(Schema):
    id=fields.Int()
    nome=fields.Str()
    video=fields.Str()
    idGrupoMuscular=fields.Int()

class ExercicioRequestSchema(Schema):
    id=fields.Int()
    nome=fields.Str()
    video=fields.Str()
    idGrupoMuscular=fields.Int()

    @validates("nome")
    def validate_name(self, value):
         if not re.match(pattern=r"^[a-zA-Z0-9_\s]+$", string=value):
            raise ValidationError("Value must contain only alphanumeric and underscore characters.")
        
class ExercicioItem(MethodResource,Resource):
    @marshal_with(ExercicioRequestSchema)
    def get(self,exercicio_id):
        try:
            exercicio = getExercicio(exercicio_id)
            if not exercicio:
                abort(404, message="Resource not found")
            return exercicio, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    def delete(self, exercicio_id):
        try:
            deleteExercicio(exercicio_id)
            return "", 204
        except UnmappedInstanceError:
            abort(404, message="Resource not found")
        except (OperationalError, IntegrityError):
            abort(500, message="Internal Server Error")
    
    @use_kwargs(ExercicioRequestSchema, location=("form"))
    @marshal_with(ExercicioResponseSchema)
    def put(self, exercicio_id, **kwargs):
        try:
            exercicio = updateExercicio(**kwargs, id=exercicio_id)
            return exercicio, 200
        except (OperationalError, IntegrityError):
           abort(500, message="Internal Server Error")

class ExercicioList(MethodResource, Resource):
    @marshal_with(ExercicioResponseSchema(many=True))
    def get(self):
        try:
            return getExercicios(), 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(ExercicioRequestSchema, location=("form"))
    @marshal_with(ExercicioResponseSchema)
    def post(self, **kwargs):
        try:
            exercicio = addExercicio(**kwargs)
            return exercicio, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
