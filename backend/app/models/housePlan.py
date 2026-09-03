from dataclasses import dataclass,field
from typing import Optional, List


@dataclass
class Room:
    room_id:int
    name:str
    room_type:str
    x:float
    y:float
    width:float
    height:float
    min_area: Optional[float]=None

    @property
    def area(self) -> float:
        return self.height * self.width

@dataclass
class FloorBoundary:
    floorBoundary_id:int
    width:float
    height:float

@dataclass
class FloorPlan:
    floor_id:int
    floor: int
    boundary: FloorBoundary
    rooms: list[Room] = field(default_factory=list)
    svg: str = ""

@dataclass
class HousePlan:
    plan_id: int
    total_area: float
    status: str
    floors: int
    floor_plan: List[FloorPlan] = field(default_factory=list)

    def get_rooms_by_floor(self, floor:int) -> List[Room]:
        res = []
        for floor_plan in self.floor_plan:
            for floor_i in floor_plan:
                if(floor_i == floor):
                    res.append(floor_i.rooms)

        return res




    
