from src.controller.LoginController import LoginItem,LoginList
from src.controller.GrupoMuscularController import GrupoMuscularItem,GrupoMuscularList
from src.controller.ExercicioController import ExercicioItem,ExercicioList
from src.controller.PessoaController import PessoaItem,PessoaList, PessoaPorIdLogin
from src.controller.TreinoController import TreinoItem,TreinoList, TreinoPorPessoa

def initialize_endpoints(api):
    api.add_resource(LoginItem,"/login/<string:login_usuario>")
    api.add_resource(LoginList,"/login")

    api.add_resource(GrupoMuscularItem,"/grupo/<int:grupo_muscular_id>")
    api.add_resource(GrupoMuscularList,"/grupo")

    api.add_resource(ExercicioItem,"/exercicio/<int:exercicio_id>")
    api.add_resource(ExercicioList,"/exercicio")

    api.add_resource(PessoaItem,"/pessoa/<int:pessoa_id>")
    api.add_resource(PessoaList,"/pessoa")
    api.add_resource(PessoaPorIdLogin,"/pessoa/login/<int:idLogin>")

    api.add_resource(TreinoItem,"/treino/<int:treino_id>")
    api.add_resource(TreinoList,"/treino")
    api.add_resource(TreinoPorPessoa, "/treino/pessoa/<int:idPessoa>")