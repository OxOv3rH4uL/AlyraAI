from dataclasses import dataclass,field
from typing import Optional, List


@dataclass
class Room:
    name:str
    room_type:str
    x:float
    y:float
    width:float
    height:float
    
    

@dataclass
class FloorBoundary:
    width:float
    height:float

@dataclass
class FloorPlan:
    floor: int
    boundary: FloorBoundary
    rooms: list[Room] = field(default_factory=list)

@dataclass
class HousePlan:
    total_area: float
    status: str
    floors: int
    floor_plan: List[FloorPlan] = field(default_factory=list)

    



    
