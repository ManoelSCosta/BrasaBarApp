# app/database/base.py

from sqlalchemy.orm import declarative_base
from sqlalchemy import inspect

class BaseMixin:
    def to_dict(self):
        """
        Converte a instância do modelo em um dicionário,
        incluindo todos os campos mapeados na tabela.
        """
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }

Base = declarative_base(cls=BaseMixin)
