from src.model.Login import Login
from src.model.Base import db

def add_login(usuario: str , senha: str) -> Login: 

    login = Login(usuario=usuario , senha=senha)

    db.session.add(login)

    db.session.commit()

    return login


def getByUsuario(usuario: str) -> Login:

    return db.session.query(Login).filter_by(usuario=usuario).first()
  

def update_login(id: int, usuario: str,senha: str ) -> Login:
    
    login = db.session.query(Login).get(id)

    login.usuario = usuario
    login.senha = senha

    db.session.commit()

    return login
