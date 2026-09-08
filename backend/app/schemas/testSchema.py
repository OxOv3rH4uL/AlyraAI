from pydantic import BaseModel, Field

class Room(BaseModel):
    name:str
    room_type:str
    x:float
    y:float
    width: float
    height: float

class FloorBoundary(BaseModel):
    width: float = Field(
        ...,
        gt=0
    )
    height: float = Field(
        ...,
        gt=0
    )


class FloorPlan(BaseModel):
    floor:int = Field(
        ...,
        ge=1
    )
    boundary: FloorBoundary
    rooms: list[Room]

class HousePlan(BaseModel):
    total_area: float = Field(
        ...,
        ge=1
    )
    status: str
    floors:int = Field(
        ...,
        ge=1
    )
    floor_plan : list[FloorPlan]
    
