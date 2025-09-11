import re
from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError
from src.service.TreinoService import addTreino, getTreinos, getTreino, updateTreino, deleteTreino

class ExercicioResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    video = fields.Str()

class TreinoResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    serie = fields.Int()
    repeticao = fields.Int()
    idPessoa = fields.Int()
    exercicio = fields.Nested(ExercicioResponseSchema, allow_none=True)


class TreinoRequestSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    serie = fields.Int()
    repeticao = fields.Int()
    idPessoa = fields.Int()
    idExercicio = fields.Int()

    @validates("nome")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_]+$", string=value):
            raise ValidationError("Value must contain only alphanumeric and underscore characters.")

class TreinoItem(MethodResource, Resource):
    @marshal_with(TreinoResponseSchema)
    def get(self, treino_id):
        try:
            treino = getTreino(treino_id)
            if not treino:
                abort(404, message="Resource not found")
            return treino, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    def delete(self, treino_id):
        try:
            deleteTreino(treino_id)
            return "", 204
        except UnmappedInstanceError:
            abort(404, message="Resource not found")
        except (OperationalError, IntegrityError):
            abort(500, message="Internal Server Error")

    @use_kwargs(TreinoRequestSchema, location="form")
    @marshal_with(TreinoResponseSchema)
    def put(self, treino_id, **kwargs):
        try:
            treino = updateTreino(**kwargs, id=treino_id)
            return treino, 200
        except (OperationalError, IntegrityError):
            abort(500, message="Internal Server Error")

class TreinoList(MethodResource, Resource):
    @marshal_with(TreinoResponseSchema(many=True))
    def get(self):
        # Obtendo o idPessoa da query string, se presente
        id_pessoa = request.args.get('idPessoa', type=int)
        try:
            return getTreinos(idPessoa=id_pessoa), 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(TreinoRequestSchema, location="form")
    @marshal_with(TreinoResponseSchema)
    def post(self, **kwargs):
        try:
            treino = addTreino(**kwargs)
            return treino, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))

class TreinoPorPessoa(MethodResource, Resource):
    @marshal_with(TreinoResponseSchema(many=True))
    def get(self, idPessoa):
        try:
            # Obtém todos os treinos de uma pessoa pelo idPessoa
            treinos = getTreinos(idPessoa=idPessoa)
            if not treinos:
                abort(404, message="Nenhum treino encontrado para essa pessoa")
            return treinos, 200
        except OperationalError:
            abort(500, message="Erro interno no servidor")
