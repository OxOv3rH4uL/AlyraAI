from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship  
from app.helpers.database import Base

if TYPE_CHECKING:
    from app.database.housePlan import HousePlanDB
    from app.database.floorBoundary import FloorBoundaryDB
    from app.database.room import RoomDB


class FloorPlanDB(Base):
    __tablename__ = "floor_plan"

    floor_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    floor : Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    svg: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    house_plan_id: Mapped[int] = mapped_column(
        ForeignKey("house_plans.plan_id"),
        nullable=False
    )

    house_plan: Mapped["HousePlanDB"] = relationship(
        back_populates="floor_plan"
    )

    boundary : Mapped["FloorBoundaryDB"] = relationship(
        back_populates="floor_plan",
        uselist = False,
        cascade="all, delete-orphan"
    )

    rooms: Mapped["RoomDB"] = relationship(
        back_populates="floor_plan",
        cascade="all, delete-orphan"
    )
