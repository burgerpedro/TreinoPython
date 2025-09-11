from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base

class GrupoMuscular(Base):
    __tablename__="grupoMuscular"

    id = Column("id",Integer,primary_key=True,)
    nome = Column("nome", String(50), nullable=False)

    exercicios = relationship("Exercicio",back_populates="grupoMuscular")
    