from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.bootstrap import redis_connector
from src.config import settings
from src.api.routers import main_router


if settings.MODE == "PROD":
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app start
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    # after app stop
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(main_router)
