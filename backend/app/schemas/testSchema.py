from pydantic import BaseModel, Field

class Room(BaseModel):
    name:str
    room_type:str
    x:float
    y:float
    width: float
    height: float

class FloorBoundary(BaseModel):
    width: float 
    height: float


class FloorPlan(BaseModel):
    floor:int
    boundary: FloorBoundary
    rooms: list[Room]

class HousePlan(BaseModel):
    total_area: float
    status: str
    floors:int
    floor_plan : list[FloorPlan]
    
