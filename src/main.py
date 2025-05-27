from fastapi import FastAPI

from src.api.routers.hotels import router as hotels_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(hotels_router)
