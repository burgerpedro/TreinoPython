from src.model.Login import Login
from src.repository.LoginRepository  import add_login,getByUsuario,update_login

def addLogin(usuario: str, senha: str) -> Login:
    if(usuario is None or usuario =="" or senha is None or senha ==""):
        raise Exception
    return add_login(usuario,senha)
    

def getLogin(usuario: str) -> Login:
    return getByUsuario(usuario)

def updateLogin(id: int , usuario: str, senha: str ):
    return update_login(id=id, usuario=usuario, senha=senha)