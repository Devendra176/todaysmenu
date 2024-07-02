from contextlib import contextmanager
from dataclasses import fields, dataclass

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import DATABASE_URI

engine = create_engine(DATABASE_URI)
DbSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()
Base.metadata = metadata


class Model(Base):
    __abstract__ = True

    def as_dict(self):
        return {
            k: getattr(self, k)
            for k in self.__table__.columns.keys()
        }

    def to_dc(self, dc: dataclass):
        return dc(**{
            f.name: getattr(self, f.name)
            for f in fields(dc)
        })


@contextmanager
def db_context():
    """
    A context manager for providing the db session
    @rtype: object
    """
    db = DbSession()
    try:
        yield db
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()
