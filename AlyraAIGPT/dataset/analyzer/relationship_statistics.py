from collections import Counter


class DatasetRelationshipStatistics:

    def __init__(self):

        self.total_houses = 0

        # Overall relationship counts
        self.relationship_counts = Counter()

        # Relationship counts by category pair
        self.relationship_by_category_pair = Counter()

        # IoU distribution by category pair
        self.iou_by_category_pair = Counter()

        self.directional_relationships = Counter()

    def add_house(self, normalized_house: dict):

        self.total_houses += 1

        regions = normalized_house["regions"]
        relationships = normalized_house["relationships"]

        for relationship in relationships:

            relationship_type = relationship["relationship"]

            # Overall relationship count
            self.relationship_counts[relationship_type] += 1

            # Get actual region labels
            region_a = regions[relationship["region_a"]]
            region_b = regions[relationship["region_b"]]

            labels_a = region_a["labels"]
            labels_b = region_b["labels"]
            for label_a in labels_a:
                for label_b in labels_b:

                    if relationship_type == "a_inside_b":

                        key = (
                            label_a,
                            label_b,
                            "inside"
                        )

                    elif relationship_type == "b_inside_a":

                        key = (
                            label_b,
                            label_a,
                            "inside"
                        )

                    elif relationship_type == "a_mostly_inside_b":

                        key = (
                            label_a,
                            label_b,
                            "mostly_inside"
                        )

                    elif relationship_type == "b_mostly_inside_a":

                        key = (
                            label_b,
                            label_a,
                            "mostly_inside"
                        )

                    else:
                        continue

                    self.directional_relationships[key] += 1

            # Category-pair statistics
            for label_a in labels_a:

                for label_b in labels_b:

                    pair = tuple(
                        sorted([label_a, label_b])
                    )

                    self.relationship_by_category_pair[
                        (pair, relationship_type)
                    ] += 1

            # IoU statistics only for overlapping regions
            if "iou" in relationship:

                bucket = self._get_iou_bucket(
                    relationship["iou"]
                )

                for label_a in labels_a:

                    for label_b in labels_b:

                        pair = tuple(
                            sorted([label_a, label_b])
                        )

                        self.iou_by_category_pair[
                            (pair, bucket)
                        ] += 1

    def _get_iou_bucket(self, iou: float):

        if iou < 0.01:
            return "< 0.01"

        elif iou < 0.05:
            return "0.01 - 0.05"

        elif iou < 0.10:
            return "0.05 - 0.10"

        elif iou < 0.20:
            return "0.10 - 0.20"

        elif iou < 0.30:
            return "0.20 - 0.30"

        else:
            return ">= 0.30"

    def summary(self):

        category_pairs = {}

        for (pair, relationship), count in (
            self.relationship_by_category_pair.items()
        ):

            pair_name = f"{pair[0]} + {pair[1]}"

            if pair_name not in category_pairs:
                category_pairs[pair_name] = {}

            category_pairs[pair_name][relationship] = count

        iou_category_pairs = {}

        for (pair, bucket), count in (
            self.iou_by_category_pair.items()
        ):

            pair_name = f"{pair[0]} + {pair[1]}"

            if pair_name not in iou_category_pairs:
                iou_category_pairs[pair_name] = {}

            iou_category_pairs[pair_name][bucket] = count

        directional = {}

        for (inside_category, container_category, relationship), count in (
            self.directional_relationships.items()
        ):
            key = (
                f"{inside_category} inside {container_category}"
            )
            if relationship == "mostly_inside":
                key = (
                    f"{inside_category} mostly_inside "
                    f"{container_category}"
                )

            directional[key] = count

        return {
            "total_houses": self.total_houses,

            "relationship_counts": dict(
                self.relationship_counts
            ),

            "relationship_by_category_pair": category_pairs,

            "iou_by_category_pair": iou_category_pairs,
            "directional_relationships":directional
        }