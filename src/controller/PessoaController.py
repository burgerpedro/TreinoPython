import re

from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError

from src.service.PessoaService import addPessoa, deletePessoa, getPessoa, getPessoaIdLogin, getPessoas, updatePessoa


class PessoaResponseSchema(Schema):
    id= fields.Int()
    nome= fields.Str()
    peso= fields.Float()
    altura= fields.Float()
    imc= fields.Float()
    idade= fields.Int() 
    idLogin= fields.Int()

class PessoaRequestSchema(Schema):
    id= fields.Int()
    nome= fields.Str()
    peso= fields.Float()
    altura= fields.Float()
    imc= fields.Float()
    idade= fields.Int() 
    idLogin= fields.Int()

    validates("nome")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_]+$", string=value):
            raise ValidationError("Nome nao pode conter caracteres especiais.")

class PessoaItem(MethodResource,Resource):
    @marshal_with(PessoaResponseSchema)
    def get(self, pessoa_id):
        try:
            pessoa = getPessoa(pessoa_id)
            if not pessoa:
                abort(404, message="Resource not found")
            return pessoa, 200
        except OperationalError:
            abort(500, message="Internal Server Error")
     
    def delete(self, pessoa_id):
        try:
            deletePessoa(pessoa_id)
            return "", 204
        except UnmappedInstanceError:
            abort(404, message="Resource not found")
        except (OperationalError, IntegrityError):
            abort(500, message="Internal Server Error")

    @use_kwargs(PessoaRequestSchema, location=("form"))
    @marshal_with(PessoaResponseSchema)
    def put(self, pessoa_id, **kwargs):
        try:
            pessoa = updatePessoa(**kwargs, id=pessoa_id)
            return pessoa, 200
        except (OperationalError, IntegrityError):
           abort(500, message="Internal Server Error")

class PessoaList(MethodResource,Resource):
    @marshal_with(PessoaResponseSchema(many = True))
    def get(self):
        try:
            return getPessoas(),200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(PessoaRequestSchema, location=("form"))
    @marshal_with(PessoaResponseSchema)
    def post(self, **kwargs):
        try:
            pessoa = addPessoa(**kwargs)
            return pessoa, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))

class PessoaPorIdLogin(MethodResource, Resource):
    @marshal_with(PessoaResponseSchema)
    def get(self, idLogin):
        try:
            pessoa = getPessoaIdLogin(idLogin)
            if not pessoa:
                abort(404, message=f"Nenhuma pessoa encontrada com idLogin {idLogin}")
            return pessoa, 200
        except OperationalError:
            abort(500, message="Internal Server Error")
        