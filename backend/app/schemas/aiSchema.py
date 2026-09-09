from pydantic import BaseModel, Field

class AIPlanRequest(BaseModel):
    description: str = Field(
        ...,
        min_length = 5,
        description = "Description of the housing idea"
    )

    


class AIRoom(BaseModel):
    name:str
    room_type:str
    x:float
    y:float
    width: float
    height: float

class AIFloorBoundary(BaseModel):
    width: float = Field(
        ...,
        gt=0
    )
    height: float = Field(
        ...,
        gt=0
    )


class AIFloorPlan(BaseModel):
    floor:int = Field(
        ...,
        ge=1
    )
    boundary: AIFloorBoundary
    rooms: list[AIRoom]

class AIPlanResponse(BaseModel):
    total_area: float = Field(
        ...,
        ge=1
    )
    status: str
    floors:int = Field(
        ...,
        ge=1
    )
    floor_plan : list[AIFloorPlan]
    
