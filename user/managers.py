from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from core.exceptions import UserAlreadyExists
from core.managers import BaseManager

from passlib.context import CryptContext

from user.models import Role, User


class RoleManager(BaseManager):
    model = Role

    def get_role(self, role: str):
        return self.db.query(self.model).filter(self.model.role == role).first()

    def create(self, role: str):
        role = self.model(
            role=role
        )
        self.db.add(role)
        self.db.commit()


class UserManager(BaseManager):
    model = User
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def is_admin(self, user: User):
        role = RoleManager(self.db).get_role('admin')
        return role in user.roles

    def is_customer(self, user):
        role = RoleManager(self.db).get_role('customer')
        return role in user.roles

    def is_restaurant_owner(self, user):
        role = RoleManager(self.db).get_role('restaurant')
        return role in user.roles

    def get_by_email(self, email):
        return self.db.query(self.model).filter(self.model.email == email).first()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)

    def authenticate_user(self, email: str, password: str):
        user = self.get_by_email(email)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    def create(self, user: User, role: str):
        try:
            role = RoleManager(self.db).get_role(role)
            user.roles.append(role)
            user.password = self.get_password_hash(user.password)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError as e:
            raise UserAlreadyExists
        return self.db.query(User).options(joinedload(User.roles)).filter_by(id=user.id).first()

