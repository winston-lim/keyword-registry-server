from datetime import datetime

from pydantic import BaseModel
import pymongo
from beanie import Document

from ..config import config, database
from ..utils import auth

class User(BaseModel):
    username: str
    deleted_at: datetime | None = None
    
class DBUser(Document, User):
    password: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Settings:
        name = "users"
        indexes = [
            "username",
            [
                ("username", pymongo.ASCENDING),
                ("deleted_at", pymongo.ASCENDING)
            ]
        ]

async def get_auth_user(username: str):
    auth_user = await DBUser.find_one(DBUser.username == username)
    return auth_user

async def create_user(username: str, password: str):
    hashed_password = auth.get_password_hash(password)
    user = DBUser(username=username, password=hashed_password, created_at=datetime.now())
    await user.insert()

def auth_user_to_user(auth_user: DBUser):
    return User(username=auth_user.username, deleted_at=auth_user.deleted_at)