from logging import info

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie


from . import config
from ..model import user

settings = config.get_settings()

async def db_lifespan(app: FastAPI):
     # Startup
    app.mongodb_client = AsyncIOMotorClient(settings.mongo_url)
    print(f"client={app.mongodb_client}")
    app.database = app.mongodb_client.get_default_database()
    print(f"database={app.database}")
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")
        
    await init_beanie(database=app.database, document_models=[user.DBUser])
    
    yield

    # Shutdown
    app.mongodb_client.close()