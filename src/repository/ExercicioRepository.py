from src.model.Exercicio import Exercicio
from src.model.Base import db

def add_exercicio(nome: str, video: str,idGrupoMuscular: int ) -> Exercicio:
    
    exercicio= Exercicio(nome=nome, video=video, idGrupoMuscular=idGrupoMuscular)

    db.session.add(exercicio)

    db.session.commit()

    return exercicio

def get_exercicios() -> list[Exercicio]:

    exercicios = db.session.query(Exercicio).all()
    
    return exercicios

def get_exercicio(id: int) -> Exercicio:

    exercicio = db.session.query(Exercicio).get(id)
    
    return exercicio

def delete_exercicio(id: int) -> Exercicio:

    exercicio = db.session.query(Exercicio).get(id)
    db.session.delete(exercicio)
    db.session.commit()

def update_exercicio(id: int, nome: str, video: str, idGrupoMuscular: int) -> Exercicio:

   exercicio = db.session.query(Exercicio).get(id)

   exercicio.nome = nome
   exercicio.video = video
   exercicio.idGrupoMuscular = idGrupoMuscular

   db.session.commit()

   return exercicio

