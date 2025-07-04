from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.bootstrap import redis_connector
from src.api.routers.auth import router as auth_router
from src.api.routers.bookings import router as bookings_router
from src.api.routers.facilities import router as facilities_router
from src.api.routers.images import router as images_router
from src.api.routers.hotels import router as hotels_router
from src.api.routers.rooms import router as hotel_rooms_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app start
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    yield
    await redis_connector.close()
    # after app stop


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router)
app.include_router(images_router)
app.include_router(hotels_router)
app.include_router(hotel_rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
