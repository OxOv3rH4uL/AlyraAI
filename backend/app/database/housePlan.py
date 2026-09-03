from typing import TYPE_CHECKING
from sqlalchemy import Float,String,Integer
from sqlalchemy.orm import Mapped, mapped_column , relationship
from app.helpers.database import Base

if TYPE_CHECKING:
    from app.database.floorPlan import FloorPlanDB
    
from typing import List

class HousePlanDB(Base):
    __tablename__ = "house_plans"

    plan_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    total_area: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    floors: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    floor_plan: Mapped[List["FloorPlanDB"]] = relationship(
        back_populates="house_plans",
        cascade="all, delete-orphan"
    )   