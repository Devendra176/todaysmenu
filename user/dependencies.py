from typing import Annotated
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from todaysmenu.user.helpers import decode_access_token, oauth2_scheme
from user.managers import UserManager
from user.schemas import TokenData
from user.models import User
from core.utils import get_db


class JWTError:
    pass


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token.__dict__["credentials"])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = UserManager(db).get_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def get_current_customer(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    if not UserManager(db).is_customer(user=current_user):
        raise HTTPException(status_code=403)
    return current_user


def get_current_restaurant_owner(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    if not UserManager(db).is_restaurant_owner(user=current_user):
        raise HTTPException(status_code=403)
    return current_user
