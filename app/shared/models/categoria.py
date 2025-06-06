from sqlalchemy import Column, String, Integer
from app.database.base import Base # noqa

class Categoria(Base):
    __tablename__ = 'bba_categoria'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
