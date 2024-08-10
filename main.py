from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .config import config, database
from .dependency import auth
from .utils import auth as auth_utils
from .model import user

settings = config.get_settings()
app = FastAPI(lifespan=database.db_lifespan)

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(auth.oauth2_scheme)]):
    return {"token": token}

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth_user = await auth.authenticate_user(form_data.username, form_data.password)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": auth_user.username}, expires_delta=access_token_expires
    )
    return auth_utils.Token(access_token=access_token, token_type="bearer")
    
@app.get("/users/me")
async def read_users_me(current_user: Annotated[user.User, Depends(auth.get_current_active_user)]):
    return current_user