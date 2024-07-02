from sqlalchemy import Column, DateTime, func

from config.db import DbSession


def get_db():
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


class TimestampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
