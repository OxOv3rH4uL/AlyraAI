from collections import defaultdict


class DatasetAnalyzer:

    def analyze(self, house: dict) -> dict:
        room_category = house["room_category"]

        all_rooms = []

        for category, boxes in room_category.items():
            for box in boxes:
                x1, y1, x2, y2 = box

                all_rooms.append({
                    "category": category,
                    "box": box,
                    "x": x1,
                    "y": y1,
                    "width": x2 - x1,
                    "height": y2 - y1
                })

        unique_boxes = self._find_unique_boxes(all_rooms)

        return {
            "house_id": house["id"],
            "room_num": house["room_num"],
            "category_entries": len(all_rooms),
            "unique_boxes": len(unique_boxes),
            "duplicate_groups": self._find_duplicate_groups(all_rooms),
            "overlap_relationships": self._find_overlap_relationships(all_rooms),
            "categories": self._category_counts(all_rooms),
            "has_negative_coordinates": self._has_negative_coordinates(all_rooms),
            "bbox": house["bbox"]
        }

    # --------------------------------------------------
    # Negative Coordinates
    # --------------------------------------------------

    def _has_negative_coordinates(self, rooms):
        for room in rooms:
            x1, y1, x2, y2 = room["box"]

            if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0:
                return True

        return False

    # --------------------------------------------------
    # Category statistics
    # --------------------------------------------------

    def _category_counts(self, rooms):
        counts = defaultdict(int)

        for room in rooms:
            counts[room["category"]] += 1

        return dict(counts)

    # --------------------------------------------------
    # Unique boxes
    # --------------------------------------------------

    def _find_unique_boxes(self, rooms):
        unique = set()

        for room in rooms:
            unique.add(tuple(room["box"]))

        return unique

    # --------------------------------------------------
    # Exact duplicate boxes
    # --------------------------------------------------

    def _find_duplicate_groups(self, rooms):
        groups = defaultdict(list)

        for room in rooms:
            groups[tuple(room["box"])].append(room["category"])

        duplicates = []

        for box, categories in groups.items():
            if len(categories) > 1:
                duplicates.append({
                    "box": list(box),
                    "categories": categories
                })

        return duplicates

    # --------------------------------------------------
    # Overlap analysis
    # --------------------------------------------------

    def _find_overlap_relationships(self, rooms):
        relationships = []

        for i, room_a in enumerate(rooms):

            for room_b in rooms[i + 1:]:

                box_a = room_a["box"]
                box_b = room_b["box"]

                metrics = self._calculate_overlap(box_a, box_b)

                if metrics is None:
                    continue

                relationships.append({
                    "room_a": room_a["category"],
                    "box_a": list(box_a),
                    "room_b": room_b["category"],
                    "box_b": list(box_b),
                    **metrics
                })

        return relationships

    def _calculate_overlap(self, box_a, box_b):

        ax1, ay1, ax2, ay2 = box_a
        bx1, by1, bx2, by2 = box_b

        # ----------------------------------------------
        # Exact identical boxes
        # ----------------------------------------------

        if box_a == box_b:
            area_a = self._area(box_a)

            return {
                "relationship": "identical",
                "intersection_area": area_a,
                "iou": 1.0,
                "overlap_percentage_a": 100.0,
                "overlap_percentage_b": 100.0
            }

        # ----------------------------------------------
        # Intersection
        # ----------------------------------------------

        intersection_width = min(ax2, bx2) - max(ax1, bx1)
        intersection_height = min(ay2, by2) - max(ay1, by1)

        if intersection_width <= 0 or intersection_height <= 0:
            return None

        intersection_area = (
            intersection_width * intersection_height
        )

        area_a = self._area(box_a)
        area_b = self._area(box_b)

        union_area = area_a + area_b - intersection_area

        iou = intersection_area / union_area

        overlap_percentage_a = (
            intersection_area / area_a
        ) * 100

        overlap_percentage_b = (
            intersection_area / area_b
        ) * 100

        # ----------------------------------------------
        # Containment
        # ----------------------------------------------

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

        if a_inside_b or b_inside_a:
            relationship = "contained"
        else:
            relationship = "partial_overlap"

        return {
            "relationship": relationship,
            "intersection_area": round(intersection_area, 4),
            "iou": round(iou, 4),
            "overlap_percentage_a": round(overlap_percentage_a, 2),
            "overlap_percentage_b": round(overlap_percentage_b, 2)
        }

    # --------------------------------------------------
    # Area
    # --------------------------------------------------

    def _area(self, box):
        x1, y1, x2, y2 = box

        width = x2 - x1
        height = y2 - y1

        return width * height