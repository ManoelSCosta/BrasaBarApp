from sqlalchemy import Column, String, Integer
from app.database.base import Base # noqa: F401

class Caixa(Base):
    __tablename__ = 'bba_caixa'
    id = Column(Integer, primary_key=True)
    data_abertura = Column(String, nullable=False)
    data_fechamento = Column(String, nullable=False)
    total = Column(String, nullable=False)

