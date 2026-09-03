from pydantic import BaseModel, Field

class PlanRequest(BaseModel):
    description: str = Field(
        ...,
        min_length = 5,
        description = "Description of the housing idea"
    )

    area_sqft : int  = Field(
        ...,
        gt=0,
        description = "Housing Area"
    )
    floors : int = Field(
        ...,
        gt=0,
        le=5,
        description = "Floors"
    )
    bedrooms : int = Field(
        ...,
        gt=0,
        le=15,
        description="No of bedrooms"
    )
    bathrooms : int = Field(
        ...,
        gt = 0,
        le=10,
        description="No of bathrooms"
    )
    style: str = Field(
        default="modern",
        description="Architecture Style"
    )


class Room(BaseModel):
    name:str
    x:float
    y:float
    width: float
    height: float

class FloorPlan(BaseModel):
    floor:int
    rooms: list[Room]
    svg:str


class PlanResponse(BaseModel):
    plan_id: str
    total_area: float
    status: str
    floors:int
    floor_plans : list[FloorPlan]
    
