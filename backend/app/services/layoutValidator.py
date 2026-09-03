from app.models.housePlan import HousePlan, Room

class LayoutValidator:
    def validate(self, plan: HousePlan) -> list[str]:
        errors =[]
        errors.extend(self.overlap_check(plan))
        errors.extend(self.dimension_check(plan))
        errors.extend(self.floor_boundary_check(plan))
        return errors

    def overlap_check(self,plan: HousePlan) -> list[str]:
        errors = []


        for floor_plan in plan.floor_plan   :
            for i,room_i in enumerate(floor_plan.rooms):
                for room_j in floor_plan.rooms[i+1]:
                    if self.overlapping(room_i,room_j):
                        res = f"{room_i.name} overlaps with {room_j.name} on floor {floor_plan.floor}"
                        errors.append(res)



        return errors

    def overlaps(self,room_a : Room, room_b: Room) -> bool:
        return (room_a.x < room_b.x + room_b.width and room_a.x + room_a.width > room_b.x and room_a.y < room_b.y + room_b.height and room_a.y + room_a.height > room_b.y)

    def dimension_check(self, plan : HousePlan) -> list[str]:
        errors = []

        for floor_plan in plan.floor_plan:
            for room in floor_plan.rooms:
                if(room.width <= 0):
                    errors.append(f"{room.name} has invalid width")
                if(room.height <= 0):
                    errors.append(f"{room.name} has invalid height")

        return errors

    def floor_boundary_check(self, plan: HousePlan) -> list[str]:
        errors = []

        for floor_plan in plan.floor_plan:
            boundaries = floor_plan.boundary
            if(boundaries.width <= 0):
                errors.append(f"Floor {floor_plan.floor} has invalid width boundary")
            if(boundaries.height <= 0):
                errors.append(f"Floor {floor_plan.floor} has invalid height boundary")

        return errors