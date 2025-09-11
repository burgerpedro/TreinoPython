from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base

class Pessoa(Base):
    __tablename__= "pessoa"

    # Columns
    id = Column("id",Integer,primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    peso = Column("peso", Float, nullable=False)
    altura = Column("altura",Float,nullable=False)
    imc = Column("imc",Float,nullable= True)
    idade=Column("idade",Integer,nullable = True)
   
    loginFK = ForeignKey("login.id" , ondelete = "SET NULL")
    idLogin=Column("idLogin",loginFK,nullable= True)

    login = relationship('Login',back_populates='pessoas',uselist= True )
    treino= relationship('Treino',back_populates='pessoas',uselist= True )