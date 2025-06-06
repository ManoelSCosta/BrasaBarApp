from sqlalchemy import Column, String, Integer
from app.database.base import Base # noqa: F401

class Pedido(Base):
    __tablename__ = 'bba_pedido'
    id = Column(Integer, primary_key=True)
    cliente = Column(String, nullable=False)
    data = Column(String, nullable=False)
    hora = Column(String, nullable=False)
    total = Column(String, nullable=False)
    status = Column(String, nullable=False)