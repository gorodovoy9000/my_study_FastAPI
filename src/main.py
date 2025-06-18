from fastapi import FastAPI

from src.api.routers.auth import router as auth_router
from src.api.routers.bookings import router as bookings_router
from src.api.routers.facilities import router as facilities_router
from src.api.routers.hotels import router as hotels_router
from src.api.routers.rooms import router as hotel_rooms_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(hotel_rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
