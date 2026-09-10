from pydantic import BaseModel, Field

class PlanRequest(BaseModel):
    description: str 



class Room(BaseModel):
    name:str
    x:float
    y:float
    width: float
    height: float

class FloorPlan(BaseModel):
    floor:int
    rooms: list[Room]


class PlanResponse(BaseModel):
    total_area: float
    status: str
    floors:int
    floor_plan: list[FloorPlan]
    svg:str
    
