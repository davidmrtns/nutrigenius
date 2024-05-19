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
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    receitas = relationship("Receita", backref="usuario", cascade="all, delete-orphan")


class Receita(database.Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    calorias = Column(Float, nullable=False)
    rendimento = Column(String(50), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    ingredientes = relationship("Ingrediente", backref="receita", cascade="all, delete-orphan")
    modo_preparo = relationship("ModoPreparo", backref="receita", cascade="all, delete-orphan")


class Ingrediente(database.Model):
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    receita_id = Column(Integer, ForeignKey("receita.id"), nullable=False)


class ModoPreparo(database.Model):
    id = Column(Integer, primary_key=True)
    passo = Column(String(100), nullable=False)
    ordem = Column(Integer, nullable=False)
    receita_id = Column(Integer, ForeignKey("receita.id"), nullable=False)
