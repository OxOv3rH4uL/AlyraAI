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
    floor: int = 1
    min_area: Optional[float]=None

    @property
    def area(self) -> float:
        return self.height * self.width


class HousePlan:
    plan_id: str
    total_area: float
    floors: int
    rooms: List[Room] = field(default_factory=list)

    def add_room(self, room: Room) -> None:
        self.rooms.append(room)

    def get_rooms_by_floor(self, floor:int) -> List[Room]:
        res = []
        for room in self.rooms:
            if room.floor == floor:
                res.append(room)
        return res


    
