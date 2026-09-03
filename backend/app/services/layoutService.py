from app.models.housePlan import HousePlan, Room
from app.schemas.planSchema import PlanRequest

class LayoutService:

    def generate_layout(self,plan:HousePlan, req: PlanRequest) -> HousePlan:
        """
        AI should generate the Layout
        """

        if plan.floors >= 1:
            self._generate_ground_floor(plan,req)

        if plan.floors >= 2:
            self._generate_upper_floor(plan,req)

        return plan

    def _generate_ground_floor(self, plan: HousePlan) -> None:
        plan.add_room(
            Room(
                name="Living Room",
                room_type="living_room",
                x=0,
                y=0,
                width=6,
                height=5,
                floor=1
            )
        )

        plan.add_room(
            Room(
                name="Kitchen",
                room_type="kitchen",
                x=6,
                y=0,
                width=4,
                height=5,
                floor=1
            )
        )

        plan.add_room(
            Room(
                name="Dining Room",
                room_type="dining_room",
                x=0,
                y=5,
                width=5,
                height=4,
                floor=1
            )
        )

    def _generate_first_floor(self, plan: HousePlan) -> None:
        plan.add_room(
            Room(
                name="Bedroom 1",
                room_type="bedroom",
                x=0,
                y=0,
                width=5,
                height=4,
                floor=2
            )
        )

        plan.add_room(
            Room(
                name="Bedroom 2",
                room_type="bedroom",
                x=5,
                y=0,
                width=5,
                height=4,
                floor=2
            )
        )