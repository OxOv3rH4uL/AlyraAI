from app.models.housePlan import HousePlan, Room

class LayoutValidator:
    def validate(self, plan: HousePlan) -> list[str]:
        errors =[]
        errors.extend(self.overlap_check(plan))
        errors.extend(self.dimension_check(plan))
        errors.extend(self.floor_boundary_check(plan))
        errors.extend(self.room_within_floor_boundary_check(plan))
        errors.extend(self.total_floor_check(plan))
        errors.extend(self.floor_number_check(plan))
        

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

    def room_within_floor_boundary_check(self,plan: HousePlan) -> list[str]:
        errors = []

        for floor_plan in plan.floor_plan:
            boundary = floor_plan.boundary
            for room in floor_plan.rooms:
                if(room.x < 0):
                    errors.append(f"{room.name} goes beyond the left boundary of the floor {floor_plan.floor}")
                if(room.y < 0):
                    errors.append(f"{room.name} goes beyond the top boundary of the floor {floor_plan.floor}")

                if(room.x + room.width > boundary.width):
                    errors.append(f"{room.name} width exceeds the floor {floor_plan.floor} width boundary")

                if(room.y + room.height > boundary.height):
                    errors.append(f"{room.name} height exceeds the floor {floor_plan.floor} height boundary")

        return errors

    def total_floor_check(self,plan : HousePlan) -> list[str]:
        errors = []
        if(len(plan.floor_plan) != plan.floors):
            errors.append(f"Expected {plan.floors} floor plans but received only {len(plan.floor_plan)} floor plans")

        return errors

    def floor_number_check(self, plan : HousePlan) -> list[str]:
        errors = []

        for floor_plan in plan.floor_plan:
            if(floor_plan.floor <= 0):
                errors.append(f"Invalid Floor Number {floor_plan.floor}")
            if(floor_plan.floor > plan.floors):
                errors.append(f"Floor {floor_plan.floor} exceeeds total number of floors {plan.floors}")

        return errors
    