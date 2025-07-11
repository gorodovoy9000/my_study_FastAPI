from src.schemas.hotels import HotelsWriteSchema


async def test_add_hotel(db):
    hotel_data = HotelsWriteSchema(title="Hotel 5 stars", location="Sochi")
    new_hotel_data = await db.hotels.add(hotel_data)
    print(f"{new_hotel_data}")
    await db.commit()
