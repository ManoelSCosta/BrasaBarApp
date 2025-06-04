from sqlalchemy import Column, String, Integer
from app.database.base import Base # noqa: F401


class Item(Base):
    __tablename__ = 'bba_item'

    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    preco = Column(String, nullable=False)