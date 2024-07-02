from pydoc import Doc
from typing import Union, Optional, List, Annotated

from fastapi import Form
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator, EmailStr

from enum import Enum

from config.db import db_context
from user.managers import UserManager


class UserLogin(BaseModel):
    email: str
    password: str


class RoleBase(BaseModel):
    role: str

    class Config:
        from_attributes = True


class UserDetails(BaseModel):
    email: str = None
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    roles: Optional[List[RoleBase]] = None

    class Config:
        from_attributes = True


class Roles(Enum):
    restaurant = "restaurant"
    customer = "customer"


class UserSignupSchema(BaseModel):
    email: Union[EmailStr, None] = None
    first_name: str
    last_name: str
    password: str
    phone: str
    role: Roles = Roles.customer

    @field_validator("email")
    def validate_email(cls, email: str):
        with db_context() as db:
            if UserManager(db).get_by_email(email):
                raise RequestValidationError(
                    errors=["Email already exists"],
                )
        return email


class TokenData(BaseModel):
    email: Union[str, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class OAuth2EmailPasswordSchema:
    def __init__(
            self,
            *,
            email: Annotated[
                str,
                Form(),
                Doc(
                ),
            ],
            password: Annotated[
                str,
                Form(),
                Doc(
                ),
            ],
    ):
        self.email = email
        self.password = password
