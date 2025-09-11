from src.model.Pessoa import Pessoa
from src.model.Base import db

def add_pessoa(nome: str,peso: float ,altura: float,imc: float,idade: int ,idLogin:None) -> Pessoa: 

    pessoa= Pessoa(nome=nome, peso=peso, altura=altura, imc=imc, idade=idade, idLogin = idLogin)

    db.session.add(pessoa)

    db.session.commit()
    
    return pessoa
    
def get_pessoas() -> list[Pessoa]:

    pessoas =db.session.query(Pessoa).all()

    return pessoas

def get_pessoa(id: int ) -> Pessoa:

    pessoa = db.session.query(Pessoa).get(id)

    return pessoa

def get_pessoa_por_idLogin(idLogin: int) -> Pessoa:

    pessoa = db.session.query(Pessoa).filter(Pessoa.idLogin == idLogin).first()
    return pessoa

def delete_pessoa(id: int) -> Pessoa:

     pessoa = db.session.query(Pessoa).get(id)
     db.session.delete(pessoa)
     db.session.commit()

def update_pessoa(id: int, nome: str, peso: float, altura: float, imc: float, idade: int , idLogin: int) -> Pessoa:

    pessoa = db.session.query(Pessoa).get(id)

    pessoa.nome = nome
    pessoa.peso = peso
    pessoa.altura = altura
    pessoa.imc = imc
    pessoa.idade = idade
    pessoa.idLogin = idLogin

    db.session.commit()

    return pessoa


