from src.model.Pessoa import Pessoa
from src.repository.PessoaRepository  import delete_pessoa, get_pessoa_por_idLogin,update_pessoa,get_pessoa,add_pessoa,get_pessoas

def addPessoa(nome: str,peso: float ,altura: float,imc: float,idade: int ,idLogin:None) -> Pessoa:     
    if(nome is None or nome == ''):
        raise Exception
    if(peso < 30 or peso =="" or peso is None):
        raise Exception
    if(altura < 1.0 or altura =="" or altura is None):
        raise Exception
    if(idade < 14 or idade =="" or idade is None):
        raise Exception
    
    return add_pessoa(nome,peso,altura,imc,idade,idLogin)
    
def getPessoas() -> list[Pessoa]:
    return get_pessoas()

def getPessoa(id: int) -> Pessoa:
    return get_pessoa(id)

def getPessoaIdLogin(idLogin: int) -> Pessoa:
    return get_pessoa_por_idLogin(idLogin)


def updatePessoa(id: int, nome: str, peso: float, altura: float, imc: float, idade: int , idLogin: int):
    return update_pessoa(id=id, nome=nome, peso=peso, altura=altura, imc=imc, idade=idade, idLogin = idLogin)

def deletePessoa(id: int):
    delete_pessoa(id)