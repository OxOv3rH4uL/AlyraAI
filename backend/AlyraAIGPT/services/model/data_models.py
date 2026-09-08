from dataclasses import dataclass,field
from typing import Optional, List


# @dataclass
# class Room:
#     room_id:int
#     name:str
#     room_type:str
#     x:float
#     y:float
#     width:float
#     height:float
#     min_area: Optional[float]=None

#     @property
#     def area(self) -> float:
#         return self.height * self.width

# @dataclass
# class FloorBoundary:
#     floorBoundary_id:int
#     width:float
#     height:float

# @dataclass
# class FloorPlan:
#     floor_id:int
#     floor: int
#     boundary: FloorBoundary
#     rooms: list[Room] = field(default_factory=list)
#     svg: str = ""

# @dataclass
# class HousePlan:
#     plan_id: int
#     total_area: float
#     status: str
#     floors: int
#     floor_plan: List[FloorPlan] = field(default_factory=list)




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
    


    
