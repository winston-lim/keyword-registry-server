from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .config import config, database
from .dependency import auth
from .model import user

settings = config.get_settings()
app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.settings = config.get_settings()
    app.mongodb_client = database.get_client()

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    database.client = None

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(auth.oauth2_scheme)]):
    return {"token": token}

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    auth_user = auth.authenticate_user(form_data.username, form_data.password)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": auth_user.username}, expires_delta=access_token_expires
    )
    return auth.Token(access_token=access_token, token_type="bearer")
    
@app.get("/users/me")
async def read_users_me(current_user: Annotated[user.User, Depends(auth.get_current_active_user)]):
    return current_user