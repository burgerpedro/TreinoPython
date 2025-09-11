from src.model.GrupoMuscular import GrupoMuscular
from src.model.Base import db

def add_grupo_muscular(nome: str) -> GrupoMuscular:

    grupo__muscular = GrupoMuscular(nome=nome)

    db.session.add(grupo__muscular)

    db.session.commit()

    return grupo__muscular

def get_grupos_musculares() -> list[GrupoMuscular]:
    
    grupos__musculares = db.session.query(GrupoMuscular).all()

    return grupos__musculares

def get_grupo_muscular_by_id(id: int) -> GrupoMuscular:
   
    grupo__muscular = db.session.query(GrupoMuscular).get(id)

    return grupo__muscular

def delete_grupo_muscular(id: int):

    grupo__muscular = db.session.query(GrupoMuscular).get(id)
    db.session.delete(grupo__muscular)
    db.session.commit()

def update_grupo_muscular(nome: str, id: int) -> GrupoMuscular:

    grupo__muscular = db.session.query(GrupoMuscular).get(id)

    grupo__muscular.nome = nome

    db.session.commit()

    return grupo__muscular