from typing import TYPE_CHECKING
from sqlalchemy import String,Integer,Float,ForeignKey
from sqlalchemy.orm import mapped_column,Mapped,relationship

if TYPE_CHECKING:
    from app.database.floorPlan import FloorPlanDB


from app.helpers.database import Base

class RoomDB(Base):
    __tablename__ = "rooms"

    room_id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    room_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    x: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    y: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    width: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    height: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    floor_plan_id: Mapped[int] = mapped_column(
        ForeignKey("floor_plan.floor_id"),
        nullable=False
    )

    floor_plan: Mapped["FloorPlanDB"] = relationship(
        back_populates="rooms"
    )

