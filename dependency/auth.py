from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from ..model import user
from ..config import config
from ..utils import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(username: str, password: str):
    auth_user = await user.get_auth_user(username)
    if not auth_user:
        return False
    if not auth.verify_password(password, auth_user.password):
        return False
    return auth_user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.get_settings().secret_key, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    auth_user = await user.get_auth_user(token_data.username)
    if auth_user is None:
        raise credentials_exception
    return user.auth_user_to_user(auth_user)
    

async def get_current_active_user(
    current_user: Annotated[user.User, Depends(get_current_user)],
):
    if current_user.deleted_at:
        raise HTTPException(status_code=401, detail="User inactive")
    return current_user