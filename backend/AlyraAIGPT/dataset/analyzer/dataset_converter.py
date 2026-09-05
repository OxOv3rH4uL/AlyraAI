# from models.house_plan import HousePlan
# from models.floor_plan import FloorPlan
# from models.floor_boundary import FloorBoundary
# from models.room import Room

# from backend.app.schemas.planSchema import Hou
from app.schemas.datasetSchema import HousePlan,FloorBoundary,FloorPlan,Room


class HousePlanConverter:

    def convert(self, normalized_house: dict) -> HousePlan:

        rooms = []

        for region in normalized_house["regions"]:

            room_type = (
                region["canonical_label"]
                if region["canonical_label"]
                else region["labels"][0]
            )

            room = Room(
                name=room_type,
                room_type=room_type,
                x=region["x"],
                y=region["y"],
                width=region["width"],
                height=region["height"],
            )

            rooms.append(room)

        boundary_data = normalized_house["boundary"]

        boundary = FloorBoundary(
            width=boundary_data["width"],
            height=boundary_data["height"]
        )

        floor_plan = FloorPlan(
            floor=1,
            boundary=boundary,
            rooms=rooms
        )

        total_area = (
            boundary.width *
            boundary.height
        )

        return HousePlan(
            total_area=total_area,
            status="normalized",
            floors=1,
            floor_plan=[floor_plan]
        )