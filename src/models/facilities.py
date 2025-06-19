from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))


FacilitiesRoomsAssociationTable = Table(
    "facilities_rooms_at",
    Base.metadata,
    Column("facility_id", ForeignKey("facilities.id", ondelete="CASCADE"), primary_key=True),
    Column("room_id", ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True),
)
