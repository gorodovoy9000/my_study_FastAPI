from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = "facilities"
    # columns
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    # relations
    rooms: Mapped[list["RoomsOrm"]] = relationship(
        secondary="facilities_rooms_at", back_populates="facilities")
