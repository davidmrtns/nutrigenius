# from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData

# Conexão com o banco de dados
engine = create_engine('sqlite:///seu_banco_de_dados.db')

metadata = MetaData()

class Usuario(metadata):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    receitas = relationship("Receita", back_populates="usuario")

class Receita(metadata):
    __tablename__ = 'receitas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    modo_preparo = Column(Text, nullable=False)
    calorias = Column(Float, nullable=False)
    rendimento = Column(String(50), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="receitas")

# Criação das tabelas
metadata.create_all(engine)