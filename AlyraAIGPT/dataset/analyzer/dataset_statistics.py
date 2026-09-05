from collections import Counter


class DatasetStatistics:

    def __init__(self):
        self.total_houses = 0

        self.room_num = []
        self.category_entries = []
        self.unique_boxes = []

        self.categories = Counter()

        self.houses_with_duplicates = 0
        self.houses_with_negative_coordinates = 0
        self.houses_with_overlaps = 0
        self.overlap_iou_buckets = Counter()

        self.identical_category_pairs = Counter()

    def add_house(self, result: dict):
        self.total_houses += 1

        self.room_num.append(result["room_num"])
        self.category_entries.append(result["category_entries"])
        self.unique_boxes.append(result["unique_boxes"])

        # Category frequency
        for category, count in result["categories"].items():
            self.categories[category] += count

        # Duplicate geometry
        if result["duplicate_groups"]:
            self.houses_with_duplicates += 1

            for group in result["duplicate_groups"]:
                categories = group["categories"]

                # Record category pairs such as:
                # Toilet + Bathroom
                for i in range(len(categories)):
                    for j in range(i + 1, len(categories)):
                        pair = tuple(sorted(
                            [categories[i], categories[j]]
                        ))
                        self.identical_category_pairs[pair] += 1

        # Negative coordinates
        for relationship in result["overlap_relationships"]:
            box_a = relationship["box_a"]
            box_b = relationship["box_b"]

            if min(box_a[0], box_a[1], box_a[2], box_a[3]) < 0:
                self.houses_with_negative_coordinates += 1
                break

            if min(box_b[0], box_b[1], box_b[2], box_b[3]) < 0:
                self.houses_with_negative_coordinates += 1
                break

        for relationship in result["overlap_relationships"]:
            if relationship["relationship"] == "identical":
                continue
            iou = relationship["iou"]

            if iou < 0.01:
                bucket = "< 0.01"
            elif iou < 0.05:
                bucket = "0.01 - 0.05"
            elif iou < 0.10:
                bucket = "0.05 - 0.10"
            elif iou < 0.20:
                bucket = "0.10 - 0.20"
            elif iou < 0.30:
                bucket = "0.20 - 0.30"
            else:
                bucket = ">= 0.30"

            self.overlap_iou_buckets[bucket] += 1
        # Overlaps
        if result["overlap_relationships"]:
            self.houses_with_overlaps += 1

    def summary(self):
        return {
            "total_houses": self.total_houses,

            "room_num": self._range_stats(self.room_num),

            "category_entries": self._range_stats(
                self.category_entries
            ),

            "unique_boxes": self._range_stats(
                self.unique_boxes
            ),

            "categories": dict(self.categories),

            "houses_with_duplicates":
                self.houses_with_duplicates,

            "houses_with_negative_coordinates":
                self.houses_with_negative_coordinates,

            "houses_with_overlaps":
                self.houses_with_overlaps,

            "overlap_iou_distribution": 
                dict(self.overlap_iou_buckets),

            "identical_category_pairs":
                {
                    str(pair): count
                    for pair, count
                    in self.identical_category_pairs.items()
                },
            "duplicate_pair_statistics": self.duplicate_pair_statistics()
        }

    def _range_stats(self, values):
        if not values:
            return {
                "min": 0,
                "max": 0,
                "average": 0
            }

        return {
            "min": min(values),
            "max": max(values),
            "average": round(
                sum(values) / len(values),
                2
            )
        }

    def duplicate_pair_statistics(self):
        results = {}

        for pair, pair_count in self.identical_category_pairs.items():

            label_a, label_b = pair

            frequency_a = self.categories[label_a]
            frequency_b = self.categories[label_b]

            ratio_a = pair_count / frequency_a if frequency_a else 0
            ratio_b = pair_count / frequency_b if frequency_b else 0

            pair_name = f"{label_a} + {label_b}"

            results[pair_name] = {
                "count": pair_count,
                f"{label_a}_frequency": frequency_a,
                f"{label_b}_frequency": frequency_b,
                f"ratio_to_{label_a}": round(ratio_a, 4),
                f"ratio_to_{label_b}": round(ratio_b, 4)
            }

        return results