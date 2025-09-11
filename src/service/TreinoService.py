
from src.model.Treino import Treino
from src.repository.TreinoRepository import update_treino, add_treino, get_treinos, get_treino, delete_treino

def addTreino(nome: str, repeticao: int, serie: int, idPessoa=None, idExercicio=None) -> Treino:
    if nome is None or nome == '':
        raise Exception("Nome inválido")
    if repeticao < 0 or serie < 0:
        raise Exception("Repetição ou série não podem ser negativos")
    return add_treino(nome, repeticao, serie, idPessoa, idExercicio)

def getTreinos(idPessoa=None) -> list[dict]:
    return get_treinos(idPessoa=idPessoa)

def getTreino(id: int) -> Treino:
    return get_treino(id)

def updateTreino(id: int, nome: str, repeticao: int, serie: int, idPessoa=None, idExercicio=None):
    return update_treino(id=id, nome=nome, serie=serie, repeticao=repeticao, idPessoa=idPessoa, idExercicio=idExercicio)

def deleteTreino(id: int):
    delete_treino(id)
