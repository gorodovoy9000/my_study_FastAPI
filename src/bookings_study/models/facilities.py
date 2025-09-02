import typing

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bookings_study.database import Base

if typing.TYPE_CHECKING:
    from bookings_study.models.rooms import RoomsOrm


class FacilitiesOrm(Base):
    __tablename__ = "facilities"
    # columns
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    # relations
    rooms: Mapped[list["RoomsOrm"]] = relationship(
        secondary="facilities_rooms_at", back_populates="facilities"
    )

    __table_args__ = (UniqueConstraint("title", name="uc_facilities-title"),)
