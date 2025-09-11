from src.model.Treino import Treino
from src.model.Base import db
from sqlalchemy.orm import joinedload

def add_treino(nome: str, repeticao: int, serie: int, idPessoa=None, idExercicio=None) -> Treino:
    treino = Treino(nome=nome, serie=serie, repeticao=repeticao, idPessoa=idPessoa, idExercicio=idExercicio)
    db.session.add(treino)
    db.session.commit()
    return treino

def get_treinos(idPessoa=None) -> list[dict]:
    query = db.session.query(Treino).options(joinedload(Treino.exercicios))
    if idPessoa:
        query = query.filter(Treino.idPessoa == idPessoa)
    
    treinos = query.all()

    # Formatar os dados com as informações do exercício
    result = []
    for treino in treinos:
        result.append({
            "id": treino.id,
            "nome": treino.nome,
            "repeticao": treino.repeticao,
            "serie": treino.serie,
            "idPessoa": treino.idPessoa,
            "exercicio": {
                "id": treino.exercicios.id if treino.exercicios else None,
                "nome": treino.exercicios.nome if treino.exercicios else None,
                "video": treino.exercicios.video if treino.exercicios else None,
            }
        })

    return result

def get_treino(id: int) -> Treino:
    treino = db.session.query(Treino).get(id)
    return treino

def delete_treino(id: int) -> Treino:
    treino = db.session.query(Treino).get(id)
    db.session.delete(treino)
    db.session.commit()

def update_treino(id: int, nome: str, repeticao: int, serie: int, idPessoa=None, idExercicio=None) -> Treino:
    treino = db.session.query(Treino).get(id)
    treino.nome = nome
    treino.repeticao = repeticao
    treino.serie = serie
    treino.idPessoa = idPessoa
    treino.idExercicio = idExercicio
    db.session.commit()
    return treino
