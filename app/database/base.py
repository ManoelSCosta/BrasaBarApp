from sqlalchemy.orm import declarative_base
class BaseMixin:
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
Base = declarative_base(cls=BaseMixin)
