from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base


class Login(Base):
    __tablename__="login"

    id = Column("id",Integer,primary_key=True,)
    usuario = Column("usuario", String(30), nullable=False)
    senha = Column("senha", String(30), nullable=False)

    pessoas = relationship("Pessoa",back_populates="login")
    