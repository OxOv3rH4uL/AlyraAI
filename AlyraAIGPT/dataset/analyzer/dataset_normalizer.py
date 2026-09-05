class HouseExpoNormalizer:

    def normalize(self, house: dict) -> dict:
        rooms = self._extract_rooms(house)
        regions = self._group_identical_boxes(rooms)
        regions = self._normalize_coordinates(regions)
        boundary = self._calculate_boundary(regions)
        # relationships = self._find_relationships(regions)
        return {
            "house_id": house["id"],
            "regions": regions,
            "boundary": boundary,
            "relationships" : self._find_relationships(regions)
        }

    def _calculate_boundary(self, regions: list) -> dict:
        if not regions:
            return {
                "width": 0,
                "height": 0
            }

        max_x = max(
            region["x"] + region["width"]
            for region in regions
        )

        max_y = max(
            region["y"] + region["height"]
            for region in regions
        )

        return {
            "width": max_x,
            "height": max_y
        }
    def _extract_rooms(self, house: dict) -> list:
        rooms = []

        for category, boxes in house["room_category"].items():
            for box in boxes:
                x1, y1, x2, y2 = box

                rooms.append({
                    "label": category,
                    "x": x1,
                    "y": y1,
                    "width": x2 - x1,
                    "height": y2 - y1
                })

        return rooms

    def _calculate_relationship(self, region_a: dict, region_b: dict):
        ax1 = region_a["x"]
        ay1 = region_a["y"]
        ax2 = ax1 + region_a["width"]
        ay2 = ay1 + region_a["height"]

        bx1 = region_b["x"]
        by1 = region_b["y"]
        bx2 = bx1 + region_b["width"]
        by2 = by1 + region_b["height"]

        intersection_width = min(ax2, bx2) - max(ax1, bx1)
        intersection_height = min(ay2, by2) - max(ay1, by1)

        # No area intersection
        if intersection_width <= 0 or intersection_height <= 0:

            horizontal_touch = (
                abs(ax2 - bx1) < 1e-6 or
                abs(bx2 - ax1) < 1e-6
            )

            vertical_overlap = (
                min(ay2, by2) - max(ay1, by1) > 0
            )

            vertical_touch = (
                abs(ay2 - by1) < 1e-6 or
                abs(by2 - ay1) < 1e-6
            )

            horizontal_overlap = (
                min(ax2, bx2) - max(ax1, bx1) > 0
            )

            if (
                (horizontal_touch and vertical_overlap)
                or
                (vertical_touch and horizontal_overlap)
            ):
                return {
                    "relationship": "adjacent"
                }

            return {
                "relationship": "separate"
            }

        # Intersection exists
        intersection_area = (
            intersection_width * intersection_height
        )

        area_a = region_a["width"] * region_a["height"]
        area_b = region_b["width"] * region_b["height"]

        union_area = area_a + area_b - intersection_area

        iou = intersection_area / union_area

        overlap_percentage_a = (
            intersection_area / area_a
        ) * 100

        overlap_percentage_b = (
            intersection_area / area_b
        ) * 100

        # Check containment
        a_inside_b = (
            ax1 >= bx1
            and ay1 >= by1
            and ax2 <= bx2
            and ay2 <= by2
        )

        b_inside_a = (
            bx1 >= ax1
            and by1 >= ay1
            and bx2 <= ax2
            and by2 <= ay2
        )

        if a_inside_b:
            relationship = "a_inside_b"

        elif b_inside_a:
            relationship = "b_inside_a"

        elif overlap_percentage_a >= 90:
            relationship = "a_mostly_inside_b"

        elif overlap_percentage_b >= 90:
            relationship = "b_mostly_inside_a"

        else:
            relationship = "partial_overlap"

        return {
            "relationship": relationship,
            "intersection_area": round(intersection_area, 4),
            "iou": round(iou, 4),
            "overlap_percentage_a": round(
                overlap_percentage_a, 2
            ),
            "overlap_percentage_b": round(
                overlap_percentage_b, 2
            )
        }

    def _find_relationships(self, regions: list) -> list:
        relationships = []

        for i in range(len(regions)):
            for j in range(i + 1, len(regions)):

                relationship = self._calculate_relationship(
                    regions[i],
                    regions[j]
                )

                relationships.append({
                    "region_a": i,
                    "region_b": j,
                    **relationship
                })

        return relationships

    def _group_identical_boxes(self, rooms: list) -> list:
        groups = {}

        for room in rooms:

            key = (
                room["x"],
                room["y"],
                room["width"],
                room["height"]
            )

            if key not in groups:
                groups[key] = {
                    "region_id" : len(groups),
                    "x": room["x"],
                    "y": room["y"],
                    "width": room["width"],
                    "height": room["height"],
                    "labels": [],
                    "canonical_label" : None
                }

            # Avoid duplicate semantic labels
            if room["label"] not in groups[key]["labels"]:
                groups[key]["labels"].append(room["label"])

        return list(groups.values())

    def _normalize_coordinates(self, regions: list) -> list:
        if not regions:
            return regions

        min_x = min(region["x"] for region in regions)
        min_y = min(region["y"] for region in regions)

        for region in regions:
            region["x"] -= min_x
            region["y"] -= min_y

        return regions