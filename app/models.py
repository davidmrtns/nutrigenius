# from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from flask_login import UserMixin
from app import database, login_manager


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    receitas = relationship("Receita", back_populates="usuario")


class Receita(database.Model):
    __tablename__ = 'receitas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    modo_preparo = Column(Text, nullable=False)
    calorias = Column(Float, nullable=False)
    rendimento = Column(String(50), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="receitas")
