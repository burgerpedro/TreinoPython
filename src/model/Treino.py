from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base

class Treino(Base):
    __tablename__= "treino"

    # Columns
    id = Column("id",Integer,primary_key=True)
    nome = Column("nome", String(50), nullable=False)
    repeticao = Column("repeticao",Integer,nullable=False)
    serie = Column("serie",Integer,nullable=False)

    pessoaFK = ForeignKey("pessoa.id", ondelete="SET NULL")
    idPessoa=Column("idPessoa",pessoaFK,nullable= True)
    exercicioFK = ForeignKey("exercicio.id", ondelete="SET NULL")
    idExercicio=Column("idExercicio",exercicioFK,nullable= True)


    pessoas = relationship('Pessoa',back_populates='treino',uselist= True )
    exercicios = relationship('Exercicio',back_populates='treinos',uselist= False )


    