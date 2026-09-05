# from pathlib import Path

from pathlib import Path
# import json

# from dataset_analyzer import DatasetAnalyzer
# from dataset_statistics import DatasetStatistics
# from relationship_statistics import DatasetRelationshipStatistics
# from dataset_normalizer import HouseExpoNormalizer


DATASET_PATH = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAI\backend\AlyraAIGPT\cleansed_data")
# DATASET_PATH = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAI\backend\AlyraAIGPT\example_data")
# # OUTPUT_FILE = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\analysis_results.txt")
# # op2 = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\statistics_results.txt")
# # op2 = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\relationship_results.txt")
# # op2 = Path(r"C:\Users\91994\OneDrive\Desktop\AlyraAIGPT\example_results.txt")


# def main():

#     analyzer = DatasetAnalyzer()
#     stat = DatasetStatistics()
#     normalizer = HouseExpoNormalizer()
#     # stat = DatasetRelationshipStatistics()  
#     json_files = list(DATASET_PATH.glob("*.json"))
#     for file in json_files:

#         with open(file, "r", encoding="utf-8") as f:
#             house = json.load(f)
#         analyzed = analyzer.analyze(house)
#         # normalized = normalizer.normalize(house)

#         stat.add_house(analyzed)

#     summary = stat.summary()

#     with open(op2, "w", encoding="utf-8") as output:
#         output.write(
#             json.dumps(summary, indent=2)
#         )

#     print(f"Analyzed {len(json_files)} houses")
#     print(f"Results saved to: {op2}")

# if __name__ == "__main__":
#     main()


# from pathlib import Path
import json
# from dataset_normalizer import HouseExpoNormalizer
# from dataset_converter import HousePlanConverter

from AlyraAIGPT.dataset.analyzer.dataset_normalizer import HouseExpoNormalizer
from AlyraAIGPT.dataset.analyzer.dataset_converter import HousePlanConverter
# from dataset_normalizer import HouseExpoNormalizer
# # from house_plan_converter import HousePlanConverter
# from dataset_converter import HousePlanConverter
from dataclasses import asdict

# DATASET_PATH = Path(
#     r"C:\Users\91994\OneDrive\Desktop\AlyraAI\AlyraAIGPT\cleansed_data"
# )

OUTPUT_PATH = Path(
    r"C:\Users\91994\OneDrive\Desktop\AlyraAI\backend\AlyraAIGPT\normalized_dataset"
)

def round_floats(data):
    if isinstance(data, float):
        return round(data, 4)

    if isinstance(data, dict):
        return {
            key: round_floats(value)
            for key, value in data.items()
        }

    if isinstance(data, list):
        return [
            round_floats(value)
            for value in data
        ]

    return data

def main():
    normalizer = HouseExpoNormalizer()
    converter = HousePlanConverter()
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    json_files = list(DATASET_PATH.glob("*.json"))
    for file in json_files:
        with open(file, "r", encoding="utf-8") as f:
            house = json.load(f)
        normalized = normalizer.normalize(house)
        house_plan = converter.convert(normalized)
        house_plan_data = asdict(house_plan)
        house_plan_data = round_floats(house_plan_data)
        output_file = OUTPUT_PATH / f"{house['id']}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                house_plan_data,
                f,
                indent=2
            )

    print(f"Processed {len(json_files)} houses")


if __name__ == "__main__":
    main()