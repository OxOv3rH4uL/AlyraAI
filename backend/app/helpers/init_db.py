from app.helpers.database import Base, engine
from app.database.housePlan import HousePlanDB
from app.database.floorPlan import FloorPlanDB
from app.database.floorBoundary import FloorBoundaryDB
from app.database.room import RoomDB




def init_db():
    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()