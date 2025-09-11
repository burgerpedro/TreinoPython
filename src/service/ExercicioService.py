from src.model.Exercicio import Exercicio
from src.repository.ExercicioRepository  import delete_exercicio, update_exercicio, add_exercicio,get_exercicios,get_exercicio

def addExercicio(nome: str, video: str,idGrupoMuscular: int ) -> Exercicio:
    if(video is None or video == '' or nome is None or nome == ''):
        raise Exception
    return add_exercicio(nome,video,idGrupoMuscular)
    
def getExercicios() -> list[Exercicio]:
    return get_exercicios()

def getExercicio(id: int) -> Exercicio:
    return get_exercicio(id)

def updateExercicio(id:int, nome: str, video: str,idGrupoMuscular: int):
    return update_exercicio(id=id, nome=nome, video=video, idGrupoMuscular=idGrupoMuscular)

def deleteExercicio(id: int):
    delete_exercicio(id)