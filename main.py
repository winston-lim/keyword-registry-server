from typing import Union

from fastapi import FastAPI

from config import config, database

settings = config.get_settings()
app = FastAPI()
db = database.get_database()

@app.get("/")
def read_root():
    return {"Hello": "World"}