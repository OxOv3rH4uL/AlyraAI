from dataclasses import dataclass,field
from typing import Optional, List


@dataclass
class Room:
    room_id: Optional[int] = None
    name:str = ""
    room_type:str = ""
    x:float = 0
    y:float = 0
    width:float = 0
    height:float = 0
    min_area: Optional[float]=None

    @property
    def area(self) -> float:
        return self.height * self.width

@dataclass
class FloorBoundary:
    floorBoundary_id: Optional[int] = None
    width:float = 0
    height:float = 0

@dataclass
class FloorPlan:
    floor_id: Optional[int] = None
    floor: int = 0
    boundary: FloorBoundary = None
    rooms: list[Room] = field(default_factory=list)
    svg: str = ""

@dataclass
class HousePlan:
    plan_id: Optional[int] = None
    total_area: float = 0
    status: str = ""
    floors: int = 0
    floor_plan: List[FloorPlan] = field(default_factory=list)

    def get_rooms_by_floor(self, floor:int) -> List[Room]:
        res = []
        for floor_plan in self.floor_plan:
            for floor_i in floor_plan:
                if(floor_i == floor):
                    res.append(floor_i.rooms)

        return res




    
