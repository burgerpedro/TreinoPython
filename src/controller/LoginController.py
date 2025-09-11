import re

from flask_restful import Resource, abort
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError
from src.service.LoginService import addLogin, getLogin, updateLogin

class LoginResponseSchema(Schema):
    id= fields.Int()
    usuario= fields.Str()
    senha =fields.Str()

class LoginResquestSchema(Schema):
    id= fields.Int()
    usuario= fields.Str()
    senha =fields.Str()

    @validates("usuario")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_]+$", string=value):
            raise ValidationError(
                "Usuario não pode ter catacteres especiais.")
        
class LoginItem(MethodResource,Resource):
    @marshal_with(LoginResponseSchema)
    def get(self, login_usuario):
        try:
            login=getLogin(login_usuario)
            if not login:
                abort(404, message="Resource not found")
            return login, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(LoginResponseSchema, location=("form"))
    @marshal_with(LoginResponseSchema)
    def put(self, login_usuario, **kwargs):
        try:
            login = updateLogin(**kwargs,usuario = login_usuario)
            return login, 200
        except (OperationalError, IntegrityError):
           abort(500, message="Internal Server Error")

class LoginList(MethodResource,Resource):
    @use_kwargs(LoginResquestSchema,location =("form"))
    @marshal_with(LoginResponseSchema)
    def post(self,**kwargs):
        try:
            login = addLogin(**kwargs)
            return login,201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))


