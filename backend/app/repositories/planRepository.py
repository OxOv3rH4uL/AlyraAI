from sqlalchemy.orm import Session
from app.models.housePlan import HousePlan
from app.database.housePlan import HousePlanDB
from app.database.floorPlan import FloorPlanDB
from app.database.floorBoundary import FloorBoundaryDB
from app.database.room import RoomDB

class PlanRepository:

    def __init__(self,db:Session):
        self.db = db

    def save(self, plan: HousePlan) -> HousePlanDB:

        house_plan = HousePlanDB(
            total_area= plan.total_area,
            status = plan.status,
            floors = plan.floors
        )
        self.db.add(house_plan)
        self.db.flush()

        for floor_plan in plan.floor_plan:

            floor_plan_db = FloorPlanDB(
                floor = floor_plan.floor,
                svg = floor_plan.svg,
                house_plan = house_plan.plan_id   
            )
            self.db.add(floor_plan_db)
            self.db.flush()

            boundary_db = FloorBoundaryDB(
                width=floor_plan.boundary.width,
                height=floor_plan.boundary.height,
                floor_plan_id = floor_plan_db.floor_id
            )
            self.db.add(boundary_db)
        
            for room in floor_plan.rooms:
                room_db = RoomDB(
                    name = room.name,
                    room_type = room.room_type,
                    x = room.x,
                    y = room.y,
                    width = room.width,
                    height = room.height
                )
                self.db.add(room_db)

        self.db.commit()
        self.db.refresh(house_plan)        