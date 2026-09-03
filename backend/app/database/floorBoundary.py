from typing import TYPE_CHECKING
from sqlalchemy import Integer,Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.helpers.database import Base

if TYPE_CHECKING:
    from app.database.floorPlan import FloorPlanDB


class FloorBoundaryDB(Base):
    __tablename__ = "floor_boundary"

    floorBoundary_id : Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    width : Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    height : Mapped[Float] = mapped_column(
        Float,
        nullable=False

    )
    floor_plan_id: Mapped[int] = mapped_column(
        ForeignKey("floor_plan.floor_id"),
        nullable=False,
        unique=True
    )
    floor_plan: Mapped["FloorPlanDB"] = relationship(
        back_populates= "boundary"
    )