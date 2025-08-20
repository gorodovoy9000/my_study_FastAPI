import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bookings_study.database import Base

if typing.TYPE_CHECKING:
    from bookings_study.models.facilities import FacilitiesOrm


class RoomsOrm(Base):
    __tablename__ = "rooms"
    # columns
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
    # relations
    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        secondary="facilities_rooms_at", back_populates="rooms"
    )
