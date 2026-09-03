from app.schemas.planSchema import PlanRequest, PlanResponse
from app.models.housePlan import HousePlan, Room
from app.services.layoutValidator import LayoutValidator
from app.services.layoutService import LayoutService
from app.services.renderingService import RenderingService

class PlanService:

    def __init__(self, layoutService: LayoutService ,validator:LayoutValidator, renderer: RenderingService):
        self.layoutService = layoutService
        self.validator = validator
        self.renderer = renderer


    def generate_plan(self, request: PlanRequest) -> PlanResponse:

        plan = HousePlan(
            plan_id="001",
            total_area=request.area_sqft,
            floors=request.floors
        )

        

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
                name="Bedroom 1",
                room_type="bedroom",
                x=0,
                y=5,
                width=5,
                height=4,
                floor=1
            )
        )
        plan.add_room(
            Room(
                name="Bedroom 2",
                room_type="bedroom",
                x=0,
                y=5,
                width=5,
                height=4,
                floor=2
            )
        )
        plan = self.layoutService.generate_layout(plan,req=request)
        errors = self.layout_validator.validate(plan)

        if errors:
            raise ValueError(
                f"Invalid generated layout: {errors}"
            )

        floor_plans = []
        for floor in range(1,plan.floors+1):
            rooms = plan.get_rooms_by_floor(floor)
            floor_plan = {
            "floor": floor,
            "rooms": [
                {
                    "name": room.name,
                    "room_type": room.room_type,
                    "x": room.x,
                    "y": room.y,
                    "width": room.width,
                    "height": room.height,
                    "floor": room.floor
                }
                for room in rooms
            ],
            "svg": self.rendering_service.render_svg(
                HousePlan(
                    plan_id=plan.plan_id,
                    total_area=plan.total_area,
                    floors=plan.floors,
                    rooms=rooms
                )
            )
        }

        floor_plans.append(floor_plan)

        rooms = [
            {
                "name": room.name,
                "x": room.x,
                "y": room.y,
                "width": room.width,
                "height": room.height,
                "floor" : room.floor
            }
            for room in plan.rooms
        ]

        return PlanResponse(
            plan_id=plan.plan_id,
            total_area=plan.total_area,
            floors = plan.floors,
            status="generated",
            floor_plans = floor_plans
        )
    