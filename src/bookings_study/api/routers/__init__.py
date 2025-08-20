from fastapi import APIRouter

from bookings_study.api.routers.auth import router as auth_router
from bookings_study.api.routers.bookings import router as bookings_router
from bookings_study.api.routers.facilities import router as facilities_router
from bookings_study.api.routers.images import router as images_router
from bookings_study.api.routers.hotels import router as hotels_router
from bookings_study.api.routers.rooms import router as hotel_rooms_router


main_router = APIRouter(prefix="/api")
# protected_router = APIRouter(dependencies=[AuthDep])
protected_router = APIRouter()
public_router = APIRouter()

# auth
public_router.include_router(auth_router)

# media files
protected_router.include_router(images_router)

# business entities
protected_router.include_router(bookings_router)
protected_router.include_router(facilities_router)
protected_router.include_router(hotels_router)
protected_router.include_router(hotel_rooms_router)

main_router.include_router(protected_router)
main_router.include_router(public_router)
