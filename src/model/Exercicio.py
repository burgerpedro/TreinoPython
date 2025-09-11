from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base

class Exercicio(Base):
    __tablename__= "exercicio"

    # Columns
    id = Column("id",Integer,primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    video = Column("video", String(200), nullable=False)
    grupoMuscularFK = ForeignKey("grupoMuscular.id", ondelete = "SET NULL")
    idGrupoMuscular=Column("idGrupoMuscular",grupoMuscularFK,nullable= True)

    grupoMuscular = relationship('GrupoMuscular',back_populates = 'exercicios',uselist = True)
    treinos = relationship('Treino',back_populates="exercicios")