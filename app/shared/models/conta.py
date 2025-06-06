from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Numeric
from sqlalchemy.orm import relationship

from app.database.base import Base

class Conta(Base):
    __tablename__ = 'bba_conta'

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    aberta = Column(Boolean, default=True)
    data_abertura = Column(DateTime, default=datetime.utcnow)
    data_fechamento = Column(DateTime)
    embalagem = Column(Boolean, default=False)
    total = Column(Numeric(10, 2), default=0.0)

    #Relacionamentos
    pedidos = relationship("Pedido", back_populates="conta")
    pagamentos = relationship("Pagamento", back_populates="conta")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.cliente,
            "tipo": self.tipo,
            "aberta": self.aberta,
            "data_abertura": self.data_abertura.isoformat() if self.data_abertura else None,
            "embalagem": self.embalagem,
            "total": self.total,
            "quantidade_pedidos": len(self.pedidos)
        }
