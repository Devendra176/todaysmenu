from sqlalchemy import Column, Integer, String, Boolean, Table, \
    ForeignKey

from sqlalchemy.orm import relationship

from config.db import Base, Model
from passlib.context import CryptContext

from core.utils import TimestampMixin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


user_role_association = Table(
    'user_role',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)


class Role(Model):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    role = Column(String, unique=True)
    users = relationship('User', secondary=user_role_association, back_populates="roles")


class User(Model, TimestampMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    roles = relationship('Role', secondary=user_role_association, back_populates="users")

    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    def set_password(self, password: str) -> None:
        self.password = pwd_context.hash(password)
