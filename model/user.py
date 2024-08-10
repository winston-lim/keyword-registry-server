from datetime import datetime

from pydantic import BaseModel

from ..config import config, database

fake_users_db = {
    "johndoe": {
        "email": "johndoe",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_verified": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": datetime.now()
    },
    "alice": {
        "email": "alice",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_verified": True,
        "created_at": datetime.now(),
    },
}

class User(BaseModel):
    email: str
    deleted_at: datetime | None = None
    
class DBUser(User):
    password: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

def get_auth_user(email: str):
    if email in fake_users_db:
        user_dict = fake_users_db[email]
        return DBUser(**user_dict)

def auth_user_to_user(auth_user: DBUser):
    return User(email=auth_user.email, deleted_at=auth_user.deleted_at)