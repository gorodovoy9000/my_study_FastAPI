from sqlalchemy import Column, ForeignKey, Table

from src.database import Base


FacilitiesRoomsM2MTable = Table(
    "facilities_rooms_at",
    Base.metadata,
    Column(
        "facility_id", ForeignKey("facilities.id", ondelete="CASCADE"), primary_key=True
    ),
    Column("room_id", ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True),
)
