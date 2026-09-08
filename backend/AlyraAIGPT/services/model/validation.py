from data_models import HousePlan, Room

class LayoutValidator:

    def validate(self, plan:HousePlan) -> list[str]:

        try:
            errors = []

            errors.extend(self.dimension_check(plan))
            errors.extend(self.floor_boundary_check(plan))
            errors.extend(self.room_within_floor_boundary_check(plan))
            errors.extend(self.total_floor_check(plan))
            errors.extend(self.floor_number_check(plan))

            return errors

        except Exception as e:
            print("\n========== VALIDATOR ERROR ==========")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Message: {e}")

            import traceback
            traceback.print_exc()

            print("=====================================\n")

            return [
                f"Validator crashed: {type(e).__name__}: {e}"
            ]

    

    def dimension_check(self, plan:HousePlan) -> list[str]:

        errors = []

        for floor_plan in plan.floor_plan:

            for room in floor_plan.rooms:

                if room.width <= 0:
                    errors.append(
                        f"{room.name} has invalid width"
                    )

                if room.height <= 0:
                    errors.append(
                        f"{room.name} has invalid height"
                    )

        return errors

    def floor_boundary_check(self, plan:HousePlan) -> list[str]:
        errors = []

        for floor_plan in plan.floor_plan:
            boundary = floor_plan.boundary
            if boundary.width <= 0:
                errors.append(
                    f"Floor {floor_plan.floor} has invalid width boundary"
                )
            if boundary.height <= 0:
                errors.append(
                    f"Floor {floor_plan.floor} has invalid height boundary"
                )

        return errors

    def room_within_floor_boundary_check(self, plan:HousePlan) -> list[str]:
        errors = []
        for floor_plan in plan.floor_plan:
            boundary = floor_plan.boundary
            for room in floor_plan.rooms:
                if room.x < 0:
                    errors.append(
                        f"{room.name} goes beyond the left boundary "
                        f"of floor {floor_plan.floor}"
                    )

                if room.y < 0:
                    errors.append(
                        f"{room.name} goes beyond the top boundary "
                        f"of floor {floor_plan.floor}"
                    )

                if room.x + room.width > boundary.width:
                    errors.append(
                        f"{room.name} width exceeds floor "
                        f"{floor_plan.floor} width boundary"
                    )

                if room.y + room.height > boundary.height:
                    errors.append(
                        f"{room.name} height exceeds floor "
                        f"{floor_plan.floor} height boundary"
                    )
        return errors

    def total_floor_check(self, plan:HousePlan) -> list[str]:
        errors = []
        if len(plan.floor_plan) != plan.floors:
            errors.append(
                f"Expected {plan.floors} floor plans but received "
                f"only {len(plan.floor_plan)} floor plans"
            )
        return errors

    def floor_number_check(self, plan:HousePlan) -> list[str]:
        errors = []
        for floor_plan in plan.floor_plan:
            if floor_plan.floor <= 0:
                errors.append(
                    f"Invalid Floor Number {floor_plan.floor}"
                )
            if floor_plan.floor > plan.floors:
                errors.append(
                    f"Floor {floor_plan.floor} exceeds total "
                    f"number of floors {plan.floors}"
                )
        return errors