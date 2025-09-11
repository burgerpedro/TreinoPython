from src.model.GrupoMuscular import GrupoMuscular
from src.repository.GrupoMuscularRepository  import delete_grupo_muscular,update_grupo_muscular, add_grupo_muscular,get_grupos_musculares,get_grupo_muscular_by_id

def addGrupoMuscular(nome: str) -> GrupoMuscular:
    if(nome is None or nome ==""):
        raise Exception
    return add_grupo_muscular(nome)
    
def getGruposMusculares() -> list[GrupoMuscular]:
    return get_grupos_musculares()

def getGrupoMuscular(id: int) -> GrupoMuscular:
    return get_grupo_muscular_by_id(id)

def updateGrupoMuscular(id: int, nome: str):
    return update_grupo_muscular(id=id, nome=nome)

def deleteGrupoMuscular(id: int):
    delete_grupo_muscular(id)