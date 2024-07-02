from datetime import timedelta, datetime
from typing import Union

import jwt
from fastapi.security import HTTPBearer

from core.settings import api_settings

oauth2_scheme = HTTPBearer()


def token_response(token: str):
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    data.update({"exp": expire})
    token = jwt.encode(data, api_settings.SECRET_KEY, algorithm=api_settings.ALGORITHM)
    return token


def decode_access_token(token: str):
    return jwt.decode(token, api_settings.SECRET_KEY, algorithms=[api_settings.ALGORITHM])
