from sqlalchemy import Column, String, Integer
from app.database.base import Base # noqa

class Pagamento:
    __tablename__ = 'bba_pagamento'
    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    valor = Column(String, nullable=False)
